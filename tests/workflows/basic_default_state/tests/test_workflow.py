from tests.workflows.basic_default_state.workflow import BasicDefaultStateWorkflow


def test_run_workflow__happy_path():
    # GIVEN a workflow that has simple inputs and state definitions
    workflow = BasicDefaultStateWorkflow()

    # WHEN we run the workflow without providing any inputs or state
    terminal_event = workflow.run()

    # THEN the workflow should have completed successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the outputs should be defaulted correctly
    assert terminal_event.outputs == {"example_input": "hello", "example_state": 5}
