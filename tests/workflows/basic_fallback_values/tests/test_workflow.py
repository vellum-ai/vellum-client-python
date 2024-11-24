from tests.workflows.basic_fallback_values.workflow import BasicFallbackValues


def test_workflow__happy_path():
    # GIVEN a workflow that defines fallback values
    workflow = BasicFallbackValues()

    # WHEN we run the workflow
    terminal_event = workflow.run()

    # THEN we should get the expected output
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs == {"final_value": "hello"}
