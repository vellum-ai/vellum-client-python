import time

from tests.workflows.background_emitter.workflow import BackgroundEmitterWorkflow


def test_workflow__happy_path():
    """
    Test that a Workflow with an expensive data emitter completes without waiting
    for the emitter to complete.
    """

    # GIVEN a workflow with an expensive data emitter
    workflow = BackgroundEmitterWorkflow()

    # WHEN the workflow is run
    start_time = time.time()
    terminal_event = workflow.run()
    end_time = time.time()

    # THEN the workflow nodes completed without blocking on the emitter
    assert terminal_event.name == "workflow.execution.fulfilled"
    # TODO: Remove this once we've resolved `terminal_event.outputs.final_value`
    # from `OutputReference[T]` to `T`.
    # https://app.shortcut.com/vellum/story/4936
    assert terminal_event.outputs.final_value < 0.02  # type: ignore[operator]

    # AND the workflow itself completed without blocking on the emitter
    assert end_time - start_time < 0.02
