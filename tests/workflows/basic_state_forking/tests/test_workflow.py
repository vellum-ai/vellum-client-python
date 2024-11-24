from tests.workflows.basic_state_forking.workflow import BasicStateForkingWorkflow


def test_workflow__happy_path():
    """
    Ensures that our Workflow that implements state forking properly such that
    the two outputs recieve the correct forked value.
    """

    # GIVEN a workflow that implements state forking
    workflow = BasicStateForkingWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN the outputs are as expected
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs == {"top": 2, "bottom": -2}
