from tests.workflows.basic_ports.multiple_invokes.workflow import Inputs, MultipleInvokesWorkflow


def test_run_workflow():
    workflow = MultipleInvokesWorkflow()
    terminal_event = workflow.run(inputs=Inputs(value="hipeilol"))

    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs == {"first_value": "hipeilol", "second_value": "hipeilol"}
