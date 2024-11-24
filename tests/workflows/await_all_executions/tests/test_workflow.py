from tests.workflows.await_all_executions.workflow import AwaitAllExecutionsWorkflow


def test_workflow__happy_path():
    """
    This test ensures that a node can AWAIT ALL executions of other nodes,
    even if those other nodes do not emit outputs.
    """

    # GIVEN a workflow with two nodes that we need to AWAIT ALL without outputs
    workflow = AwaitAllExecutionsWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.final_value == "Hello, World!"
