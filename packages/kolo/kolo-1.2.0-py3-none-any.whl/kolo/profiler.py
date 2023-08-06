import json
import logging
import os
import subprocess
import sys
import time
import types
import uuid
from importlib import import_module
from itertools import starmap
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    TYPE_CHECKING,
    Union,
)
import traceback

import django
from django.db import connection, models, reset_queries
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from . import __version__
from .db import save_invocation_in_sqlite
from .serialize import (
    monkeypatch_queryset_repr,
    serialize_locals,
    serialize_potential_json,
)


logger = logging.getLogger("kolo")
cwd = os.getcwd()


if TYPE_CHECKING:
    from typing import TypedDict
    from typing_extensions import Protocol

    class ApiRequest(TypedDict):
        method: str
        url: str
        method_and_full_url: str
        body: Optional[str]
        headers: Dict[str, str]
        timestamp: str

    class ApiResponse(TypedDict):
        timestamp: str
        body: str
        status_code: int
        headers: Dict[str, str]

    class ApiInfo(TypedDict, total=False):
        request: ApiRequest
        response: ApiResponse

    class CeleryJob(TypedDict):
        name: str
        args: Tuple[Any, ...]
        kwargs: Dict[str, Any]

    class QueryInfo(TypedDict, total=False):
        query: str
        user_code_callsite: UserCodeCallSite
        call_timestamp: float
        return_timestamp: float

    class UserCodeCallSite(TypedDict):
        line_number: int
        call_frame_id: str

    class FrameInfo(TypedDict):
        id: str
        path: str
        co_name: str
        event: str
        arg: str
        locals: str
        timestamp: float
        user_code_callsite: Optional[UserCodeCallSite]

    class ExceptionFrameInfo(TypedDict):
        path: str
        co_name: str
        locals: str
        expanded_locals: Dict[str, str]

    class RecordedException(TypedDict):
        # Usually contains one string. Last string in the list is always
        # the one indicating which exception occurred
        exception_summary: List[str]
        exception_with_traceback: List[str]
        exception_frames: List[ExceptionFrameInfo]
        bottom_exception_frame: ExceptionFrameInfo

    class FrameFilter(Protocol):
        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

    class AdvancedFrameFilter(Protocol):
        data: Dict[str, Any]
        use_frames_of_interest: bool

        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

        def process(
            self,
            frame: types.FrameType,
            event: str,
            arg: object,
            call_frame_ids: List[Dict[str, str]],
        ):
            pass

    ProtoFrameFilter = Union[str, FrameFilter, Dict[str, str]]


class HasPath:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return self.path in frame.f_code.co_filename

    def __repr__(self):
        return f'HasPath("{self.path}")'

    def __eq__(self, other):
        return self.path == other.path


def build_frame_filter(filter: "ProtoFrameFilter") -> "FrameFilter":
    if isinstance(filter, str):
        return HasPath(filter)
    if isinstance(filter, dict):
        filter_path = filter["callable"]
        module_path, _sep, filter_name = filter_path.rpartition(".")
        module = import_module(module_path)
        return getattr(module, filter_name)
    return filter


class CeleryFilter:
    use_frames_of_interest = True

    def __init__(self) -> None:
        self.data: Dict[str, List[CeleryJob]] = {"jobs_enqueued": []}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        filepath = frame.f_code.co_filename
        return (
            "celery" in filepath
            and "sentry_sdk" not in filepath
            and "apply_async" in frame.f_code.co_name
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "return":
            return

        frame_locals = frame.f_locals
        task_name = frame_locals["self"].name
        task_args = frame_locals["args"]
        task_kwargs = frame_locals["kwargs"]

        job: CeleryJob = {"name": task_name, "args": task_args, "kwargs": task_kwargs}

        self.data["jobs_enqueued"].append(job)


def frame_path(frame: types.FrameType) -> str:
    relative_path = frame.f_code.co_filename.replace(f"{cwd}/", "")
    return f"{relative_path}:{frame.f_lineno}"


class ExceptionFilter:
    use_frames_of_interest = False

    def __init__(self) -> None:
        self.data: Dict[str, RecordedException] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        filepath = frame.f_code.co_filename
        return (
            "django" in filepath and "handle_uncaught_exception" == frame.f_code.co_name
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "return":
            # In this case both call and return frames contain what we need
            # so we just need to process one of them
            return

        frame_locals = frame.f_locals
        exc_type, exc_value, exc_traceback = frame_locals["exc_info"]

        recorded_exception_frames = []
        expanded_locals_for_frames = []
        for frame_and_line in traceback.walk_tb(exc_traceback):
            frame = frame_and_line[0]

            if not library_filter(frame):
                frame_locals = frame.f_locals

                expanded_locals = {}
                for key, value in frame_locals.items():
                    if hasattr(value, "__dict__") and isinstance(value, models.Model):
                        expanded_locals[key] = vars(value)

                recorded_exception_frames.append(frame)
                expanded_locals_for_frames.append(expanded_locals)

        def serialize_exception_frame(frame, expanded_locals) -> "ExceptionFrameInfo":
            return {
                "path": frame_path(frame),
                "co_name": frame.f_code.co_name,
                "locals": serialize_locals(frame.f_locals),
                "expanded_locals": {
                    key: serialize_locals(value)
                    for key, value in expanded_locals.items()
                },
            }

        exception_with_traceback = traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )

        zipped_frames = zip(recorded_exception_frames, expanded_locals_for_frames)
        exception_frames = list(starmap(serialize_exception_frame, zipped_frames))

        self.data["exception"] = {
            "exception_summary": traceback.format_exception_only(exc_type, exc_value),
            "exception_with_traceback": exception_with_traceback,
            "exception_frames": exception_frames,
            "bottom_exception_frame": exception_frames[-1],
        }


class SQLQueryFilter:
    use_frames_of_interest = False

    def __init__(self) -> None:
        self.queries_with_call_site: List[QueryInfo] = []
        self.data = {"queries_with_call_site": self.queries_with_call_site}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        return (
            co_name in ("_execute", "debug_sql", "execute")
            and "/django/db/backends/utils.py" in frame.f_code.co_filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        co_name = frame.f_code.co_name
        if event == "call" and co_name == "_execute":
            query_data: QueryInfo = {
                "user_code_callsite": get_callsite_data(frame, call_frame_ids[-1]),
                "call_timestamp": time.time(),
            }
            self.queries_with_call_site.append(query_data)
        elif event == "return":
            query_data = self.queries_with_call_site[-1]

            assert frame.f_back is not None
            calling_co_name = frame.f_back.f_code.co_name
            if co_name == "_execute":
                query_data["return_timestamp"] = time.time()
            elif (
                co_name == "debug_sql" and calling_co_name == "__exit__"
            ) or django.VERSION < (3, 0, 0):
                query_data["query"] = frame.f_locals["sql"]


def decode_header_value(bytes_or_str: Union[bytes, str]) -> str:
    """
    Convert a bytes header value to text.

    Valid header values are expected to be ascii in modern times, but
    ISO-8859-1 (latin1) has historically been allowed.

    https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode("latin1")
    return bytes_or_str


class ApiRequestFilter:
    use_frames_of_interest = True

    def __init__(self) -> None:
        self.data: Dict[str, List[ApiInfo]] = {"api_requests_made": []}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return self.match_request(frame) or self.match_response(frame)

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "call" and self.match_request(frame):
            self.process_api_request_made(frame)
        elif event == "return" and self.match_response(frame):
            self.process_api_response(frame)

    def match_request(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return "urllib3/connectionpool" in filepath and callable_name == "urlopen"

    def match_response(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return "requests/sessions" in filepath and "request" == callable_name

    def process_api_request_made(self, frame: types.FrameType):
        frame_locals = frame.f_locals

        scheme = frame_locals["self"].scheme
        host = frame_locals["self"].host
        url = frame_locals["url"]
        full_url = f"{scheme}://{host}{url}"

        request_headers = {
            key: decode_header_value(value)
            for key, value in frame_locals["headers"].items()
        }

        request_body = frame_locals["body"]

        try:
            json.dumps(request_body)
        except TypeError:
            if isinstance(request_body, bytes):
                body = request_body.decode("utf-8")
            else:
                body = (
                    f"Error: Could not parse request body. Type: {type(request_body)}"
                )
        else:
            body = request_body

        method = frame_locals["method"].upper()
        method_and_full_url = f"{method} {full_url}"

        api_request: ApiInfo = {
            "request": {
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "body": body,
                "headers": request_headers,
                "timestamp": timezone.now().isoformat(),
            }
        }

        self.data["api_requests_made"].append(api_request)

    def process_api_response(self, frame: types.FrameType):
        frame_locals = frame.f_locals

        method = frame_locals["method"].upper()
        url = frame_locals["prep"].url
        method_and_full_url = f"{method} {url}"

        relevant_api_request = None
        negative_target_index = None

        api_requests_made = self.data["api_requests_made"]
        for index, api_request in enumerate(reversed(api_requests_made), start=1):
            if method_and_full_url == api_request["request"]["method_and_full_url"]:
                if "response" not in api_request:
                    relevant_api_request = api_request
                    negative_target_index = index

        if relevant_api_request is not None:
            response = frame_locals["resp"]

            relevant_api_request["response"] = {
                "timestamp": timezone.now().isoformat(),
                "body": response.text,
                "status_code": response.status_code,
                "headers": dict(response.headers),
            }

            assert negative_target_index is not None
            api_requests_made[-negative_target_index] = relevant_api_request
        else:
            logger.debug(f"No matching request found for {method_and_full_url}")


def library_filter(frame: types.FrameType, *args, **kwargs) -> bool:
    """
    Ignore library code

    We want to not show library calls, so attempt to filter them out here.
    """
    filepath = frame.f_code.co_filename
    return (
        "lib/python" in filepath
        or "lib/pypy" in filepath
        or "/PyPy/" in filepath
        or "/site-packages/" in filepath
    )


def exec_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore a frame running a string executed using exec

    We can't show especially interesting information about it, so we skip it.

    A namedtuple is a common example of this case.
    """
    return frame.f_code.co_filename == "<string>"


def attrs_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore attrs generated code

    The attrs library constructs an artificial filename for generated
    class methods like __init__ and __hash__.
    """
    return frame.f_code.co_filename.startswith("<attrs generated")


def import_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore import machinery

    The import system uses frozen modules, which don't have the same
    "lib/python" string fragment in their filepath as the standard
    library or third party code.
    """
    import_modules = (
        "<frozen importlib._bootstrap>",
        "<frozen importlib._bootstrap_external>",
        "<frozen zipimport>",
        "<builtin>/frozen importlib._bootstrap_external",
        "<builtin>/frozen _structseq",
    )
    return frame.f_code.co_filename in import_modules


def kolo_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """Don't profile kolo code"""
    filename = frame.f_code.co_filename
    return "/kolo/profiler" in filename or "/kolo/serialize" in filename


def get_call_frame(
    frame: types.FrameType, filepath: str, co_name: str
) -> types.FrameType:
    """Search back in a frame's stack for the triggering user code frame"""

    while True:
        assert frame.f_back is not None
        frame = frame.f_back
        if frame.f_code.co_filename == filepath and frame.f_code.co_name == co_name:
            return frame


def get_callsite_data(
    frame: types.FrameType, call_frame_data: Dict[str, str]
) -> "UserCodeCallSite":
    """
    Find the parent user code frame and return its frame_id and line number

    We already have the frame_id available in call_frame_data, but we don't
    know the currently active line number, so we search back in the frame
    stack using the filepath and co_name until we find the call frame itself.
    """
    call_frame = get_call_frame(
        frame, call_frame_data["filepath"], call_frame_data["co_name"]
    )
    return {
        "call_frame_id": call_frame_data["frame_id"],
        "line_number": call_frame.f_lineno,
    }


class KoloProfiler:
    """
    Collect runtime information about code to view in VSCode.

    include_frames can be passed to enable profiling of standard library
    or third party code.

    ignore_frames can also be passed to disable profiling of a user's
    own code.

    The list should contain fragments of the path to the relevant files.
    For example, to include profiling for the json module the include_frames
    could look like ["/json/"].

    The list may also contain frame filters. A frame filter is a function
    (or other callable) that takes the same arguments as the profilefunc
    passed to sys.setprofile and returns a boolean representing whether
    to allow or block the frame.

    include_frames takes precedence over ignore_frames. A frame that
    matches an entry in each list will be profiled.
    """

    def __init__(self, db_path: Path, *, include_frames=(), ignore_frames=()) -> None:
        self.db_path = db_path
        self.timestamp = timezone.now()
        self.invocation_id = f"inv_{uuid.uuid4()}"
        self.frames_of_interest: List[FrameInfo] = []
        self.request: Optional[Dict[str, Any]] = None
        self.response: Optional[Dict[str, Any]] = None
        self.sql_queries_made: List[Any] = []
        self.include_frames = list(map(build_frame_filter, include_frames))
        self.ignore_frames = list(map(build_frame_filter, ignore_frames))
        self.default_include_frames: List[AdvancedFrameFilter] = [
            CeleryFilter(),
            ApiRequestFilter(),
            ExceptionFilter(),
            SQLQueryFilter(),
        ]
        self.default_ignore_frames: List[FrameFilter] = [
            library_filter,
            exec_filter,
            attrs_filter,
            import_filter,
            kolo_filter,
        ]
        self.call_frame_ids: List[Dict[str, str]] = []

    def initialize_request(self, request: HttpRequest):
        reset_queries()
        self.request = {
            "scheme": request.scheme,
            "method": request.method,
            "path_info": request.path_info,
            "body": request.body.decode("utf-8"),
            "headers": dict(request.headers),
        }

    def finalize_response(self, response: HttpResponse) -> None:
        duration = timezone.now() - self.timestamp

        self.response = {
            "ms_duration": round(duration.total_seconds() * 1000, 2),
            "status_code": response.status_code,
            "content": response.content.decode(response.charset),
            "headers": dict(response.items()),
        }
        self.sql_queries_made = connection.queries

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> None:
        if event in ["c_call", "c_return"]:
            return

        with monkeypatch_queryset_repr():
            for frame_filter in self.include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        self.process_frame(frame, event, arg)
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in include_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in ignore_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.default_include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        if frame_filter.use_frames_of_interest:
                            self.process_frame(frame, event, arg)
                        frame_filter.process(frame, event, arg, self.call_frame_ids)
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in default_include_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.default_ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in default_ignore_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            try:
                self.process_frame(frame, event, arg)
            except Exception as e:
                logger.debug(
                    "Unexpected exception in KoloProfiler.process_frame",
                    exc_info=e,
                )

    def __enter__(self):
        sys.setprofile(self)

    def __exit__(self, *exc):
        sys.setprofile(None)

    def save_request_in_db(self) -> None:
        current_commit_sha = (
            subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
            .stdout.decode("utf-8")
            .strip()
        )
        json_data = {
            "request_id": self.invocation_id,
            "invocation_id": self.invocation_id,
            "current_commit_sha": current_commit_sha,
            "request": self.request,
            "response": self.response,
            "timestamp": str(self.timestamp),
            "sql_queries_made": self.sql_queries_made,
            "frames_of_interest": self.frames_of_interest,
            "meta": {"version": __version__},
        }
        for frame_filter in self.default_include_frames:
            json_data.update(frame_filter.data)

        save_invocation_in_sqlite(
            self.db_path, self.invocation_id, json.dumps(json_data)
        )

    def process_frame(self, frame: types.FrameType, event: str, arg: object) -> None:
        user_code_callsite: Optional[UserCodeCallSite]
        if event == "call" and self.call_frame_ids:
            user_code_callsite = get_callsite_data(frame, self.call_frame_ids[-1])
        else:
            # If we are a return frame, we don't bother duplicating
            # information for the call frame.
            # If we are the first call frame, we don't have a callsite.
            user_code_callsite = None

        frame_id = f"frm_{uuid.uuid4()}"
        co_name = frame.f_code.co_name
        if event == "call":
            call_frame_data = {
                "frame_id": frame_id,
                "filepath": frame.f_code.co_filename,
                "co_name": co_name,
            }
            self.call_frame_ids.append(call_frame_data)
        elif event == "return":  # pragma: no branch
            self.call_frame_ids.pop()

        self.frames_of_interest.append(
            {
                "id": frame_id,
                "path": frame_path(frame),
                "co_name": co_name,
                "event": event,
                "arg": serialize_potential_json(arg),
                "locals": serialize_locals(frame.f_locals),
                "timestamp": time.time(),
                "user_code_callsite": user_code_callsite,
            }
        )
