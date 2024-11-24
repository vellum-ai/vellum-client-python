from tests.workflows.basic_await_all.workflow import BasicAwaitAllWorkflow, Inputs


def test_workflow__concurrent():
    # GIVEN a workflow with two nodes that we need to AWAIT ALL
    workflow = BasicAwaitAllWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=Inputs(sleep=0.0))

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.final_value == "hello world"


def test_workflow__deterministic():
    # GIVEN a workflow with two nodes that we need to AWAIT ALL
    workflow = BasicAwaitAllWorkflow()

    # WHEN we run the workflow such that one branch always finishes first
    terminal_event = workflow.run(inputs=Inputs(sleep=0.001))

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.final_value == "hello world"
