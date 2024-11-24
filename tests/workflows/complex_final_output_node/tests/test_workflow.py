from tests.workflows.complex_final_output_node.missing_final_output_node import (
    Inputs as MissingFinalOutputNodeInputs,
    MissingFinalOutputNodeWorkflow,
)
from tests.workflows.complex_final_output_node.missing_workflow_output import (
    Inputs as MissingWorkflowOutputInputs,
    MissingWorkflowOutputWorkflow,
)


def test_workflow__missing_final_output_node():
    # GIVEN a workflow with a missing terminal node
    workflow = MissingFinalOutputNodeWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=MissingFinalOutputNodeInputs(alpha="hello", beta="world"))

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"alpha": "hello", "beta": "world"}


def test_workflow__missing_workflow_output():
    # GIVEN a workflow with a missing terminal node
    workflow = MissingWorkflowOutputWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=MissingWorkflowOutputInputs(alpha="hello", beta="world"))

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"alpha": "hello"}
