# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .prompt_block_state import PromptBlockState
from .ephemeral_prompt_cache_config import EphemeralPromptCacheConfig
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class FunctionDefinition(UniversalBaseModel):
    """
    A block that represents a function definition in a prompt template.
    """

    state: typing.Optional[PromptBlockState] = None
    cache_config: typing.Optional[EphemeralPromptCacheConfig] = None
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    parameters: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None
    forced: typing.Optional[bool] = None
    strict: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow