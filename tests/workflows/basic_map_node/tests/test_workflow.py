from vellum.workflows.events.types import CodeResourceDefinition
from vellum.workflows.workflows.event_filters import all_workflow_event_filter

from tests.workflows.basic_map_node.workflow import Inputs, Iteration, IterationSubworkflow, SimpleMapExample


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


def test_map_node_streaming_events():
    """
    Ensure that we can stream the events of a Workflow that contains a MapNode,
    with a particular focus on ensuring that the events and their parent contexts are correct.
    """
    # GIVEN a workflow with a map node
    workflow = SimpleMapExample()

    # WHEN we stream the workflow events
    events = list(workflow.stream(inputs=Inputs(fruits=["apple", "banana"]), event_filter=all_workflow_event_filter))

    # THEN we see the expected events in the correct relative order
    workflow_initiated_events = [e for e in events if e.name == "workflow.execution.initiated"]
    node_initiated_events = [e for e in events if e.name == "node.execution.initiated"]
    node_fulfilled_events = [e for e in events if e.name == "node.execution.fulfilled"]
    workflow_fulfilled_events = [e for e in events if e.name == "workflow.execution.fulfilled"]
    workflow_snapshotted_events = [e for e in events if e.name == "workflow.execution.snapshotted"]

    # Main workflow initiated event
    assert workflow_initiated_events[0].workflow_definition == SimpleMapExample
    assert workflow_initiated_events[0].parent is None

    # Subworkflow initiated events
    assert len(workflow_initiated_events) == 3  # Main + 2 subworkflows
    for event in workflow_initiated_events[1:]:
        assert event.workflow_definition == IterationSubworkflow
        assert event.parent is not None
        assert event.parent.type == "WORKFLOW_NODE"
        assert event.parent.parent is not None
        assert event.parent.parent.type == "WORKFLOW"
        assert event.parent.parent.workflow_definition == CodeResourceDefinition.encode(SimpleMapExample)

        # Node initiated events
    assert len(node_initiated_events) == 3  # MapNode + 2 iterations
    assert node_initiated_events[0].parent is not None
    assert node_initiated_events[0].parent.type == "WORKFLOW"
    assert node_initiated_events[0].parent.workflow_definition == CodeResourceDefinition.encode(SimpleMapExample)

    for event in node_initiated_events[1:]:
        assert event.node_definition == Iteration
        assert event.parent is not None
        assert event.parent.type == "WORKFLOW"
        assert event.parent.workflow_definition == CodeResourceDefinition.encode(IterationSubworkflow)

    # Node fulfilled events
    assert len(node_fulfilled_events) == 3  # MapNode + 2 iterations
    for i, event in enumerate(node_fulfilled_events[:-1]):
        assert event.node_definition == Iteration
        assert event.outputs.count == len(["apple", "banana"][i]) + i

    # Final MapNode fulfilled event
    assert node_fulfilled_events[-1].outputs.count == [5, 7]

    # Workflow fulfilled events
    assert len(workflow_fulfilled_events) == 3  # Main + 2 subworkflows
    assert workflow_fulfilled_events[-1].outputs == {"final_value": [5, 7]}
    assert workflow_fulfilled_events[-1].parent is None

    # Workflow snapshotted events
    assert len(workflow_snapshotted_events) > 0
    # Total number of events is correct
    expected_events = (
        len(workflow_initiated_events)
        + len(node_initiated_events)
        + len(node_fulfilled_events)
        + len(workflow_fulfilled_events)
        + len(workflow_snapshotted_events)
    )
    assert len(events) == expected_events
