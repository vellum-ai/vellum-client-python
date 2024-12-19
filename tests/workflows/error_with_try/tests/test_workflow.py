from vellum.workflows.errors.types import WorkflowErrorCode

from tests.workflows.error_with_try.workflow import ErrorWithTryWorkflow, Inputs


def test_workflow__error_node_rejects():
    """
    Show that the workflow will reject with the same error output
    from the TryNode that routed to the ErrorNode.
    """

    # GIVEN a workflow with an error node
    workflow = ErrorWithTryWorkflow()

    # WHEN the workflow is run with a threshold that triggers the error node
    terminal_event = workflow.run(inputs=Inputs(threshold=4))

    # THEN the workflow will reject
    assert terminal_event.name == "workflow.execution.rejected"

    # AND the error message will be the one defined in the error node
    assert terminal_event.error.message == "This is a flaky node"
    assert terminal_event.error.code == WorkflowErrorCode.INVALID_OUTPUTS
