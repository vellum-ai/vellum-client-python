from tests.workflows.await_all_loops.workflow import AwaitAllWithLoopsWorkflow


def test_workflow__happy_path():
    """
    This test ensures that we can AWAIT ALL executions of multiple nodes,
    even if those nodes are inside of loops.
    """

    # GIVEN a workflow with two nodes that we need to AWAIT ALL without outputs
    workflow = AwaitAllWithLoopsWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.final_value == 3
