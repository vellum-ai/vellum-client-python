from tests.workflows.basic_execution_counter.workflow import BasicExecutionCounterWorkflow


def test_workflow__happy_path():
    # GIVEN a workflow that reference's a node's execution count
    workflow = BasicExecutionCounterWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs == {"final_value": 1}
