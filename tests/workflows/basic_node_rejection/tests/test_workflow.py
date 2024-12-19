from vellum.workflows.errors import WorkflowErrorCode

from tests.workflows.basic_node_rejection.workflow import BasicRejectedWorkflow


def test_run_workflow__happy_path():
    # GIVEN a workflow that references a node that will fail
    workflow = BasicRejectedWorkflow()

    # WHEN the workflow is run
    terminal_event = workflow.run()

    # THEN the workflow should complete with a rejection event
    assert terminal_event.name == "workflow.execution.rejected", terminal_event

    # AND the output error message should be as expected
    assert terminal_event.error.code == WorkflowErrorCode.USER_DEFINED_ERROR
    assert terminal_event.error.message == "Node was rejected"
