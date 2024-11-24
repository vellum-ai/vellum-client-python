from tests.workflows.basic_inputs_and_outputs.workflow import BasicInputsAndOutputsWorkflow, Inputs


def test_run_workflow__happy_path():
    # GIVEN a basic workflow that references inputs
    workflow = BasicInputsAndOutputsWorkflow()

    # WHEN we run the workflow with a specific set of inputs
    terminal_event = workflow.run(inputs=Inputs(initial_value=2))

    # THEN the workflow runs to completion and produces the expected outputs
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"final_value": 9}


def test_run_workflow__multiple_runs():
    # GIVEN a basic workflow that references inputs
    workflow = BasicInputsAndOutputsWorkflow()

    # WHEN we run the workflow twice with different sets of inputs
    terminal_event_1 = workflow.run(inputs=Inputs(initial_value=2))
    terminal_event_2 = workflow.run(inputs=Inputs(initial_value=3))

    # THEN the workflow runs to completion and produces the expected outputs
    assert terminal_event_1.name == "workflow.execution.fulfilled", terminal_event_1
    assert terminal_event_1.outputs == {"final_value": 9}

    assert terminal_event_2.name == "workflow.execution.fulfilled", terminal_event_2
    assert terminal_event_2.outputs == {"final_value": 16}
