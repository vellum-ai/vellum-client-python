# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .fulfilled_enum import FulfilledEnum
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class FunctionCall(UniversalBaseModel):
    """
    The final resolved function call value.
    """

    arguments: typing.Dict[str, typing.Optional[typing.Any]]
    id: typing.Optional[str] = None
    name: str
    state: typing.Optional[FulfilledEnum] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
