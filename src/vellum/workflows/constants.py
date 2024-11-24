from enum import Enum
from typing import Any, cast


class _UndefMeta(type):
    def __repr__(cls) -> str:
        return "UNDEF"

    def __getattribute__(cls, name: str) -> Any:
        if name == "__class__":
            # ensures that UNDEF.__class__ == UNDEF
            return cls

        return super().__getattribute__(name)

    def __bool__(cls) -> bool:
        return False


class UNDEF(metaclass=_UndefMeta):
    pass


LATEST_RELEASE_TAG = "LATEST"

OMIT = cast(Any, ...)


class APIRequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


class AuthorizationType(Enum):
    BEARER_TOKEN = "BEARER_TOKEN"
    API_KEY = "API_KEY"
