from tests.workflows.basic_looping.workflow import BasicLoopingWorkflow


def test_workflow__happy_path():
    # GIVEN a workflow that defines a loop
    workflow = BasicLoopingWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.final_value == 13
    assert terminal_event.outputs.node_execution_count == 5
