from tests.workflows.basic_state_management.workflow import BasicStateManagement


def test_run_workflow__happy_path():
    # GIVEN a workflow that uses State with a derived value and writable value
    workflow = BasicStateManagement()

    # WHEN the workflow is run
    terminal_event = workflow.run()

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled"

    # AND the final value should be read from the written state
    assert terminal_event.outputs == {"final_value": 3}
