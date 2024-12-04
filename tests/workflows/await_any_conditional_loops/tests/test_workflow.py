import pytest

from tests.workflows.await_any_conditional_loops.workflow import AwaitAnyWithConditionalLoopsWorkflow


@pytest.mark.skip(reason="TODO: https://app.shortcut.com/vellum/story/5729")
def test_workflow__happy_path():
    """
    This test ensures that the Workflow completes successfully with a trickier AWAIT_ANY example.
    """

    # GIVEN a Workflow with a trickier AWAIT_ANY example
    workflow = AwaitAnyWithConditionalLoopsWorkflow()

    # WHEN the Workflow is run
    final_event = workflow.run()

    # THEN the Workflow completes successfully
    assert final_event.name == "workflow.execution.fulfilled"
    assert final_event.outputs.final_value == 1
