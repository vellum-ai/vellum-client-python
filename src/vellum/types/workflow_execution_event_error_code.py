# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class WorkflowExecutionEventErrorCode(str, enum.Enum):
    """
    * `WORKFLOW_INITIALIZATION` - WORKFLOW_INITIALIZATION
    * `NODE_EXECUTION_COUNT_LIMIT_REACHED` - NODE_EXECUTION_COUNT_LIMIT_REACHED
    * `INTERNAL_SERVER_ERROR` - INTERNAL_SERVER_ERROR
    * `NODE_EXECUTION` - NODE_EXECUTION
    * `LLM_PROVIDER` - LLM_PROVIDER
    * `INVALID_TEMPLATE` - INVALID_TEMPLATE
    """

    WORKFLOW_INITIALIZATION = "WORKFLOW_INITIALIZATION"
    NODE_EXECUTION_COUNT_LIMIT_REACHED = "NODE_EXECUTION_COUNT_LIMIT_REACHED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    NODE_EXECUTION = "NODE_EXECUTION"
    LLM_PROVIDER = "LLM_PROVIDER"
    INVALID_TEMPLATE = "INVALID_TEMPLATE"

    def visit(
        self,
        workflow_initialization: typing.Callable[[], T_Result],
        node_execution_count_limit_reached: typing.Callable[[], T_Result],
        internal_server_error: typing.Callable[[], T_Result],
        node_execution: typing.Callable[[], T_Result],
        llm_provider: typing.Callable[[], T_Result],
        invalid_template: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is WorkflowExecutionEventErrorCode.WORKFLOW_INITIALIZATION:
            return workflow_initialization()
        if self is WorkflowExecutionEventErrorCode.NODE_EXECUTION_COUNT_LIMIT_REACHED:
            return node_execution_count_limit_reached()
        if self is WorkflowExecutionEventErrorCode.INTERNAL_SERVER_ERROR:
            return internal_server_error()
        if self is WorkflowExecutionEventErrorCode.NODE_EXECUTION:
            return node_execution()
        if self is WorkflowExecutionEventErrorCode.LLM_PROVIDER:
            return llm_provider()
        if self is WorkflowExecutionEventErrorCode.INVALID_TEMPLATE:
            return invalid_template()