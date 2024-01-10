# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class VellumErrorCodeEnum(str, enum.Enum):
    """
    - `INVALID_REQUEST` - INVALID_REQUEST
    - `PROVIDER_ERROR` - PROVIDER_ERROR
    - `INTERNAL_SERVER_ERROR` - INTERNAL_SERVER_ERROR
    """

    INVALID_REQUEST = "INVALID_REQUEST"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

    def visit(
        self,
        invalid_request: typing.Callable[[], T_Result],
        provider_error: typing.Callable[[], T_Result],
        internal_server_error: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is VellumErrorCodeEnum.INVALID_REQUEST:
            return invalid_request()
        if self is VellumErrorCodeEnum.PROVIDER_ERROR:
            return provider_error()
        if self is VellumErrorCodeEnum.INTERNAL_SERVER_ERROR:
            return internal_server_error()