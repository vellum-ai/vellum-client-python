from vellum.workflows.errors.types import WorkflowErrorCode

from tests.workflows.basic_error_node.workflow import BasicErrorNodeWorkflow, Inputs


def test_workflow__error_node_rejects():
    """
    Show that the workflow will reject if the error node is reached.
    """

    # GIVEN a workflow with an error node
    workflow = BasicErrorNodeWorkflow()

    # WHEN the workflow is run with a threshold that triggers the error node
    terminal_event = workflow.run(inputs=Inputs(threshold=5))

    # THEN the workflow will reject
    assert terminal_event.name == "workflow.execution.rejected"

    # AND the error message will be the one defined in the error node
    assert terminal_event.error.message == "Input threshold was too low"
    assert terminal_event.error.code == WorkflowErrorCode.USER_DEFINED_ERROR
