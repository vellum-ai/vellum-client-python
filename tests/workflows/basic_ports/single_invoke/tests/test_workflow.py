from tests.workflows.basic_ports.single_invoke.workflow import Inputs, SingleInvokeWorkflow


def test_run_workflow():
    workflow = SingleInvokeWorkflow()
    terminal_event = workflow.run(inputs=Inputs(value="world"))

    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs == {"value": "world"}
