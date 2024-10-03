# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value_request import ArrayVellumValueRequest
from .vellum_value_request import VellumValueRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class MetadataResolverVariableRequest(UniversalBaseModel):
    value: VellumValueRequest
    id: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValueRequest, MetadataResolverVariableRequest=MetadataResolverVariableRequest)