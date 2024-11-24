from tests.workflows.basic_passthrough_node.workflow import BasicPassthroughWorkflow, Inputs


def test_workflow__happy_path():
    # GIVEN a workflow that just passes through its input
    workflow = BasicPassthroughWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=Inputs(value="hello"))

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"value": "hello", "cascaded_value": "hello"}
