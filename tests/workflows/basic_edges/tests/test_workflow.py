from tests.workflows.basic_edges.workflow import BasicEdgesWorkflow


def test_run_workflow__happy_path():
    # GIVEN a workflow that has simple nodes connected by an edge
    workflow = BasicEdgesWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN the workflow should have completed successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the outputs should be defaulted correctly
    assert terminal_event.outputs == {"final_value": "Hello, World!"}
