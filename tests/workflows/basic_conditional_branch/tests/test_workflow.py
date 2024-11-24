from tests.workflows.basic_conditional_branch.workflow import BasicConditionalBranchWorkflow, Inputs
from vellum.workflows.constants import UNDEF


def test_run_workflow__branch_a():
    workflow = BasicConditionalBranchWorkflow()

    terminal_event = workflow.run(inputs=Inputs(value=True))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.branch_a == "Branch A"
    assert terminal_event.outputs.branch_b is UNDEF


def test_run_workflow__branch_b():
    workflow = BasicConditionalBranchWorkflow()

    terminal_event = workflow.run(inputs=Inputs(value=False))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.branch_b == "Branch B"
    assert terminal_event.outputs.branch_a is UNDEF
