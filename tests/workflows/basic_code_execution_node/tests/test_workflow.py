from vellum import CodeExecutorResponse, NumberVellumValue

from tests.workflows.basic_code_execution_node.try_workflow import TrySimpleCodeExecutionWorkflow
from tests.workflows.basic_code_execution_node.workflow import SimpleCodeExecutionWithFilepathWorkflow


def test_run_workflow__happy_path(vellum_client):
    # GIVEN a workflow that references a Code Execution example
    workflow = SimpleCodeExecutionWithFilepathWorkflow()

    # AND we know what the Code Execution Node will respond with
    mock_code_execution = CodeExecutorResponse(
        log="hello",
        output=NumberVellumValue(value=0),
    )
    vellum_client.execute_code.return_value = mock_code_execution

    # WHEN the workflow is run
    final_event = workflow.run()

    # THEN the workflow should complete successfully
    assert final_event.name == "workflow.execution.fulfilled", final_event

    # AND the output should match the mapped items
    assert final_event.outputs == {"result": 0, "log": "hello"}


def test_run_workflow__try_wrapped(vellum_client):
    # GIVEN a workflow that references a Code Execution example
    workflow = TrySimpleCodeExecutionWorkflow()

    # AND we know what the Code Execution Node will respond with
    mock_code_execution = CodeExecutorResponse(
        log="hello",
        output=NumberVellumValue(value=0),
    )
    vellum_client.execute_code.return_value = mock_code_execution

    # WHEN the workflow is run
    final_event = workflow.run()

    # THEN the workflow should complete successfully
    assert final_event.name == "workflow.execution.fulfilled", final_event

    # AND the output should match the mapped items
    assert final_event.outputs == {"result": 0, "log": "hello"}
