import sys

from IPython.extensions.autoreload import superreload

from tests.workflows.ipython_reload.workflow import ReloadableWorkflow


def test_run_workflow__happy_path():
    """
    Confirm that a workflow in ipython shells work as expected, even after the module is autoreloaded.
    """

    # GIVEN a workflow using an edge
    workflow = ReloadableWorkflow()

    # AND the workflow has been run once and succeeded
    terminal_event = workflow.run()
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"final_value": "Hello world"}

    # WHEN we reload the workflow in ipython
    base_module = __name__.split(".")[:-2]
    module = sys.modules.get(".".join(base_module + ["workflow"]))
    superreload(module)

    # AND we run the workflow again
    workflow = ReloadableWorkflow()
    terminal_event = workflow.run()

    # THEN the workflow succeeds again
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"final_value": "Hello world"}
