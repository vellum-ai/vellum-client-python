# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .chat_message_role import ChatMessageRole
from .content_type import ContentType


class PromptTemplateBlockPropertiesRequest(pydantic.BaseModel):
    chat_role: typing.Optional[ChatMessageRole]
    chat_message_unterminated: typing.Optional[bool]
    template: typing.Optional[str]
    template_type: typing.Optional[ContentType]
    function_name: typing.Optional[str]
    function_description: typing.Optional[str]
    function_parameters: typing.Optional[typing.Dict[str, typing.Any]]
    function_forced: typing.Optional[bool]
    blocks: typing.Optional[typing.List[PromptTemplateBlockRequest]]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}


from .prompt_template_block_request import PromptTemplateBlockRequest  # noqa: E402

PromptTemplateBlockPropertiesRequest.update_forward_refs()