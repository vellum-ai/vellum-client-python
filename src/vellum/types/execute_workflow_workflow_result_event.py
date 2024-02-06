# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .fulfilled_execute_workflow_workflow_result_event import FulfilledExecuteWorkflowWorkflowResultEvent
from .rejected_execute_workflow_workflow_result_event import RejectedExecuteWorkflowWorkflowResultEvent


class ExecuteWorkflowWorkflowResultEvent_Fulfilled(FulfilledExecuteWorkflowWorkflowResultEvent):
    state: typing_extensions.Literal["FULFILLED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ExecuteWorkflowWorkflowResultEvent_Rejected(RejectedExecuteWorkflowWorkflowResultEvent):
    state: typing_extensions.Literal["REJECTED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


ExecuteWorkflowWorkflowResultEvent = typing.Union[
    ExecuteWorkflowWorkflowResultEvent_Fulfilled, ExecuteWorkflowWorkflowResultEvent_Rejected
]