# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .chat_message_request import ChatMessageRequest


class SubmitWorkflowExecutionActualRequest_String(pydantic_v1.BaseModel):
    output_id: typing.Optional[str] = None
    output_key: typing.Optional[str] = None
    quality: typing.Optional[float] = None
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = None
    timestamp: typing.Optional[float] = None
    desired_output_value: typing.Optional[str] = None
    output_type: typing.Literal["STRING"] = "STRING"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


class SubmitWorkflowExecutionActualRequest_Json(pydantic_v1.BaseModel):
    output_id: typing.Optional[str] = None
    output_key: typing.Optional[str] = None
    quality: typing.Optional[float] = None
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = None
    timestamp: typing.Optional[float] = None
    desired_output_value: typing.Optional[typing.Dict[str, typing.Any]] = None
    output_type: typing.Literal["JSON"] = "JSON"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


class SubmitWorkflowExecutionActualRequest_ChatHistory(pydantic_v1.BaseModel):
    output_id: typing.Optional[str] = None
    output_key: typing.Optional[str] = None
    quality: typing.Optional[float] = None
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = None
    timestamp: typing.Optional[float] = None
    desired_output_value: typing.Optional[typing.List[ChatMessageRequest]] = None
    output_type: typing.Literal["CHAT_HISTORY"] = "CHAT_HISTORY"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


SubmitWorkflowExecutionActualRequest = typing.Union[
    SubmitWorkflowExecutionActualRequest_String,
    SubmitWorkflowExecutionActualRequest_Json,
    SubmitWorkflowExecutionActualRequest_ChatHistory,
]
