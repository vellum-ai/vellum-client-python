# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .function_call_chat_message_content_request import FunctionCallChatMessageContentRequest
from .image_chat_message_content_request import ImageChatMessageContentRequest
from .string_chat_message_content_request import StringChatMessageContentRequest


class ArrayChatMessageContentItemRequest_String(StringChatMessageContentRequest):
    type: typing_extensions.Literal["STRING"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayChatMessageContentItemRequest_FunctionCall(FunctionCallChatMessageContentRequest):
    type: typing_extensions.Literal["FUNCTION_CALL"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayChatMessageContentItemRequest_Image(ImageChatMessageContentRequest):
    type: typing_extensions.Literal["IMAGE"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


ArrayChatMessageContentItemRequest = typing.Union[
    ArrayChatMessageContentItemRequest_String,
    ArrayChatMessageContentItemRequest_FunctionCall,
    ArrayChatMessageContentItemRequest_Image,
]
