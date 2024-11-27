import pytest
from datetime import datetime
import json
from uuid import UUID

from deepdiff import DeepDiff

from vellum.workflows.errors.types import VellumError, VellumErrorCode
from vellum.workflows.events.node import NodeExecutionInitiatedBody, NodeExecutionInitiatedEvent
from vellum.workflows.events.types import NodeParentContext, WorkflowParentContext
from vellum.workflows.events.workflow import (
    WorkflowExecutionFulfilledBody,
    WorkflowExecutionFulfilledEvent,
    WorkflowExecutionInitiatedBody,
    WorkflowExecutionInitiatedEvent,
    WorkflowExecutionRejectedBody,
    WorkflowExecutionRejectedEvent,
    WorkflowExecutionStreamingBody,
    WorkflowExecutionStreamingEvent,
)
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.outputs.base import BaseOutput
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class MockInputs(BaseInputs):
    foo: str


class MockNode(BaseNode):
    node_foo = MockInputs.foo

    class Outputs(BaseNode.Outputs):
        example: str


class MockWorkflow(BaseWorkflow[MockInputs, BaseState]):
    graph = MockNode


name_parts = __name__.split(".")
module_root = name_parts[: name_parts.index("events")]


@pytest.mark.parametrize(
    ["event", "expected_json"],
    [
        (
            WorkflowExecutionInitiatedEvent(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                trace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                body=WorkflowExecutionInitiatedBody(
                    workflow_definition=MockWorkflow,
                    inputs=MockInputs(foo="bar"),
                ),
            ),
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "api_version": "2024-10-25",
                "timestamp": "2024-01-01T12:00:00",
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "span_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "workflow.execution.initiated",
                "body": {
                    "workflow_definition": {
                        "name": "MockWorkflow",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "inputs": {
                        "foo": "bar",
                    },
                },
                "parent": None,
            },
        ),
        (
            NodeExecutionInitiatedEvent(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                trace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                body=NodeExecutionInitiatedBody(
                    node_definition=MockNode,
                    inputs={
                        MockNode.node_foo: "bar",
                    },
                ),
                parent=NodeParentContext(
                    node_definition=MockNode,
                    span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                    parent=WorkflowParentContext(
                        workflow_definition=MockWorkflow,
                        span_id=UUID("123e4567-e89b-12d3-a456-426614174000")
                    )
                )
            ),
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "api_version": "2024-10-25",
                "timestamp": "2024-01-01T12:00:00",
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "span_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "node.execution.initiated",
                "body": {
                    "node_definition": {
                        "name": "MockNode",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "inputs": {
                        "node_foo": "bar",
                    },
                },
                "parent": {
                    "node_definition": {
                        "name": "MockNode",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "parent": {
                        "workflow_definition": {
                            "name": "MockWorkflow",
                            "module": module_root + ["events", "tests", "test_event"],
                        },
                        "type": "WORKFLOW",
                        "parent": None,
                        "span_id": "123e4567-e89b-12d3-a456-426614174000"
                    },
                    "type": "WORKFLOW_NODE",
                    "span_id": "123e4567-e89b-12d3-a456-426614174000"
                },
            },
        ),
        (
            WorkflowExecutionStreamingEvent(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                trace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                body=WorkflowExecutionStreamingBody(
                    workflow_definition=MockWorkflow,
                    output=BaseOutput(
                        name="example",
                        value="foo",
                    ),
                ),
            ),
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "api_version": "2024-10-25",
                "timestamp": "2024-01-01T12:00:00",
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "span_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "workflow.execution.streaming",
                "body": {
                    "workflow_definition": {
                        "name": "MockWorkflow",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "output": {
                        "name": "example",
                        "value": "foo",
                    },
                },
                "parent": None
            },
        ),
        (
            WorkflowExecutionFulfilledEvent(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                trace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                body=WorkflowExecutionFulfilledBody(
                    workflow_definition=MockWorkflow,
                    outputs=MockNode.Outputs(
                        example="foo",
                    ),
                ),
            ),
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "api_version": "2024-10-25",
                "timestamp": "2024-01-01T12:00:00",
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "span_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "workflow.execution.fulfilled",
                "body": {
                    "workflow_definition": {
                        "name": "MockWorkflow",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "outputs": {
                        "example": "foo",
                    },
                },
                "parent": None,
            },
        ),
        (
            WorkflowExecutionRejectedEvent(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                trace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                span_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                body=WorkflowExecutionRejectedBody(
                    workflow_definition=MockWorkflow,
                    error=VellumError(
                        message="Workflow failed",
                        code=VellumErrorCode.USER_DEFINED_ERROR,
                    ),
                ),
            ),
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "api_version": "2024-10-25",
                "timestamp": "2024-01-01T12:00:00",
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "span_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "workflow.execution.rejected",
                "body": {
                    "workflow_definition": {
                        "name": "MockWorkflow",
                        "module": module_root + ["events", "tests", "test_event"],
                    },
                    "error": {
                        "message": "Workflow failed",
                        "code": "USER_DEFINED_ERROR",
                    },
                },
                "parent": None,
            },
        ),
    ],
    ids=[
        "workflow.execution.initiated",
        "node.execution.initiated",
        "workflow.execution.streaming",
        "workflow.execution.fulfilled",
        "workflow.execution.rejected",
    ],
)
def test_event_serialization(event, expected_json):
    assert not DeepDiff(json.loads(event.model_dump_json()), expected_json)
