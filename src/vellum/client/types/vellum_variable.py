# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value import ArrayVellumValue
from .vellum_variable_type import VellumVariableType
import typing
from .vellum_value import VellumValue
from .vellum_variable_extensions import VellumVariableExtensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class VellumVariable(UniversalBaseModel):
    id: str
    key: str
    type: VellumVariableType
    required: typing.Optional[bool] = None
    default: typing.Optional[VellumValue] = None
    extensions: typing.Optional[VellumVariableExtensions] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValue, VellumVariable=VellumVariable)
