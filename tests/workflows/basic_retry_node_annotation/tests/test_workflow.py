from tests.workflows.basic_retry_node_annotation.workflow import SimpleRetryExample


def test_run_workflow__happy_path():
    # GIVEN a workflow that references a Retry example
    workflow = SimpleRetryExample()

    # WHEN the workflow is run
    terminal_event = workflow.run()

    # THEN the workflow should complete successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the output should match the environment variable
    assert terminal_event.outputs == {"final_value": 3}
