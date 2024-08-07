# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .fulfilled_prompt_execution_meta import FulfilledPromptExecutionMeta
from .initiated_prompt_execution_meta import InitiatedPromptExecutionMeta
from .prompt_output import PromptOutput
from .rejected_prompt_execution_meta import RejectedPromptExecutionMeta
from .streaming_prompt_execution_meta import StreamingPromptExecutionMeta
from .vellum_error import VellumError


class ExecutePromptEvent_Initiated(pydantic_v1.BaseModel):
    meta: typing.Optional[InitiatedPromptExecutionMeta] = None
    execution_id: str
    state: typing.Literal["INITIATED"] = "INITIATED"

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


class ExecutePromptEvent_Streaming(pydantic_v1.BaseModel):
    output: PromptOutput
    output_index: int
    execution_id: str
    meta: typing.Optional[StreamingPromptExecutionMeta] = None
    raw: typing.Optional[typing.Dict[str, typing.Any]] = None
    state: typing.Literal["STREAMING"] = "STREAMING"

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


class ExecutePromptEvent_Fulfilled(pydantic_v1.BaseModel):
    outputs: typing.List[PromptOutput]
    execution_id: str
    meta: typing.Optional[FulfilledPromptExecutionMeta] = None
    state: typing.Literal["FULFILLED"] = "FULFILLED"

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


class ExecutePromptEvent_Rejected(pydantic_v1.BaseModel):
    error: VellumError
    execution_id: str
    meta: typing.Optional[RejectedPromptExecutionMeta] = None
    state: typing.Literal["REJECTED"] = "REJECTED"

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


ExecutePromptEvent = typing.Union[
    ExecutePromptEvent_Initiated,
    ExecutePromptEvent_Streaming,
    ExecutePromptEvent_Fulfilled,
    ExecutePromptEvent_Rejected,
]
