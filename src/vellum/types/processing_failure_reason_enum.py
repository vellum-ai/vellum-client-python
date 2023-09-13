# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ProcessingFailureReasonEnum(str, enum.Enum):
    """
    * `EXCEEDED_CHARACTER_LIMIT` - Exceeded Character Limit
    * `INVALID_FILE` - Invalid File
    """

    EXCEEDED_CHARACTER_LIMIT = "EXCEEDED_CHARACTER_LIMIT"
    INVALID_FILE = "INVALID_FILE"

    def visit(
        self, exceeded_character_limit: typing.Callable[[], T_Result], invalid_file: typing.Callable[[], T_Result]
    ) -> T_Result:
        if self is ProcessingFailureReasonEnum.EXCEEDED_CHARACTER_LIMIT:
            return exceeded_character_limit()
        if self is ProcessingFailureReasonEnum.INVALID_FILE:
            return invalid_file()