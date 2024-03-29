# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .fulfilled_execute_prompt_event import FulfilledExecutePromptEvent
from .initiated_execute_prompt_event import InitiatedExecutePromptEvent
from .rejected_execute_prompt_event import RejectedExecutePromptEvent
from .streaming_execute_prompt_event import StreamingExecutePromptEvent


class ExecutePromptEvent_Initiated(InitiatedExecutePromptEvent):
    state: typing_extensions.Literal["INITIATED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ExecutePromptEvent_Streaming(StreamingExecutePromptEvent):
    state: typing_extensions.Literal["STREAMING"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ExecutePromptEvent_Fulfilled(FulfilledExecutePromptEvent):
    state: typing_extensions.Literal["FULFILLED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ExecutePromptEvent_Rejected(RejectedExecutePromptEvent):
    state: typing_extensions.Literal["REJECTED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


ExecutePromptEvent = typing.Union[
    ExecutePromptEvent_Initiated,
    ExecutePromptEvent_Streaming,
    ExecutePromptEvent_Fulfilled,
    ExecutePromptEvent_Rejected,
]
