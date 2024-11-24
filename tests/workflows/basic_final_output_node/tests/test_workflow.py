from tests.workflows.basic_final_output_node.workflow import BasicFinalOutputNodeWorkflow, Inputs


def test_workflow__happy_path():
    # GIVEN a workflow that just passes through its input to a terminal node
    workflow = BasicFinalOutputNodeWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=Inputs(input="hello"))

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"value": "hello"}
