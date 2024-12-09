from typing import cast

from vellum.workflows.events import NodeEvent
from vellum.workflows.events.types import CodeResourceDefinition
from vellum.workflows.events.workflow import WorkflowExecutionInitiatedEvent
from vellum.workflows.workflows.event_filters import all_workflow_event_filter

from tests.workflows.basic_map_node.workflow import Inputs, SimpleMapExample


def test_run_workflow__happy_path():
    # GIVEN a workflow that references a Map example
    workflow = SimpleMapExample()

    # WHEN the workflow is run
    terminal_event = workflow.run(inputs=Inputs(fruits=["apple", "banana", "date"]))

    # THEN the workflow should complete successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the output should match the mapped items
    assert terminal_event.outputs == {"final_value": [5, 7, 6]}

    # Assert that parent is a valid field, for now empty
    assert terminal_event.parent is None


def test_map_node_parent_context() -> None:
    # GIVEN a workflow with a map node
    workflow = SimpleMapExample()

    # WHEN we stream the workflow events
    events = list(workflow.stream(inputs=Inputs(fruits=["apple", "banana"]), event_filter=all_workflow_event_filter))

    # THEN we should see the expected parent context hierarchy in events
    workflow_initiated_events = [
        cast(WorkflowExecutionInitiatedEvent, e) for e in events if e.name == "workflow.execution.initiated"
    ]

    # Main workflow initiated event should have no parent
    assert workflow_initiated_events[0].workflow_definition == SimpleMapExample
    assert workflow_initiated_events[0].parent is None

    # Subworkflow initiated events should have MapNode as parent
    subworkflow_events = [cast(NodeEvent, e) for e in events if e.name.startswith("node")]
    for event in subworkflow_events:

        # Parent's parent should be the main workflow context
        assert event.parent is not None
        assert event.parent.type == "WORKFLOW"
        assert event.parent.workflow_definition == CodeResourceDefinition.encode(SimpleMapExample)

    # Verify we got events for both mapped items
    assert len(subworkflow_events) == 2
