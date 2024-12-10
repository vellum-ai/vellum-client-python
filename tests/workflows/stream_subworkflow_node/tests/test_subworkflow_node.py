from vellum.workflows.events.types import CodeResourceDefinition, NodeParentContext, WorkflowParentContext
from vellum.workflows.workflows.event_filters import all_workflow_event_filter

from tests.workflows.stream_subworkflow_node.workflow import (
    InnerWorkflow,
    Inputs,
    StreamingInlineSubworkflowExample,
    SubworkflowNode,
)


def test_workflow_stream__happy_path():
    """
    Ensure that we can stream the events of a Workflow that contains an InlineSubworkflowNode,
    with a particular focus on ensuring that the definitions and parent contexts of the events are correct.
    """

    # GIVEN a Workflow with an InlineSubworkflowNode
    workflow = StreamingInlineSubworkflowExample()

    # WHEN we stream the events of the Workflow
    stream = workflow.stream(
        inputs=Inputs(items=["apple", "banana", "cherry"]),
        event_filter=all_workflow_event_filter,
    )
    events = list(stream)

    # THEN we see the expected events in the correct relative order with proper parent contexts
    # workflow initiated events
    workflow_initiated_events = [e for e in events if e.name.startswith("workflow.execution.initiated")]
    node_initiated_events = [e for e in events if e.name.startswith("node.execution.initiated")]

    assert workflow_initiated_events[0].workflow_definition == StreamingInlineSubworkflowExample
    assert workflow_initiated_events[0].parent is None
    assert workflow_initiated_events[1].workflow_definition == InnerWorkflow
    assert isinstance(workflow_initiated_events[1].parent, NodeParentContext)
    assert workflow_initiated_events[1].parent.node_definition == CodeResourceDefinition.encode(SubworkflowNode)
    assert isinstance(workflow_initiated_events[1].parent.parent, WorkflowParentContext)
    assert workflow_initiated_events[1].parent.parent.workflow_definition == CodeResourceDefinition.encode(
        StreamingInlineSubworkflowExample
    )
    assert len(workflow_initiated_events) == 2

    # node initiated events
    assert node_initiated_events[0].node_definition == SubworkflowNode
    assert isinstance(node_initiated_events[0].parent, WorkflowParentContext)
    assert node_initiated_events[0].parent.workflow_definition == CodeResourceDefinition.encode(
        StreamingInlineSubworkflowExample
    )
    assert node_initiated_events[0].parent.parent is None
    assert len(node_initiated_events) == 1

    # inner node streaming events
    inner_node_streaming_events = [
        e for e in events if e.name.startswith("workflow.execution.") and e.workflow_definition == InnerWorkflow
    ]
    for event in inner_node_streaming_events:
        assert event.parent.type == "WORKFLOW_NODE"
        assert event.parent.node_definition == CodeResourceDefinition.encode(SubworkflowNode)
        assert event.parent.parent.type == "WORKFLOW"
        assert event.parent.parent.workflow_definition == CodeResourceDefinition.encode(
            StreamingInlineSubworkflowExample
        )

    assert inner_node_streaming_events[1].output.name == "processed"
    assert inner_node_streaming_events[1].output.is_initiated
    assert inner_node_streaming_events[2].output.delta == "apple apple"
    assert inner_node_streaming_events[3].output.delta == "banana banana"
    assert inner_node_streaming_events[4].output.delta == "cherry cherry"
    assert inner_node_streaming_events[5].output.value == [
        "apple apple",
        "banana banana",
        "cherry cherry",
    ]
    assert len(inner_node_streaming_events) == 7
