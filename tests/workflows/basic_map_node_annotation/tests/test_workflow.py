from tests.workflows.basic_map_node_annotation.workflow import Inputs, SimpleMapExample


def test_run_workflow__happy_path():
    # GIVEN a workflow that references a Map example
    workflow = SimpleMapExample()

    # WHEN the workflow is run
    terminal_event = workflow.run(inputs=Inputs(fruits=["apple", "banana", "date"]))

    # THEN the workflow should complete successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the output should match the mapped items
    assert terminal_event.outputs == {"final_value": [5, 7, 6]}
