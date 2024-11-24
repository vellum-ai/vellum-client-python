from tests.workflows.basic_conditional_node.workflow import CategoryWorkflow, Inputs
from vellum.workflows.constants import UNDEF


def test_run_workflow__question():
    workflow = CategoryWorkflow()

    terminal_event = workflow.run(inputs=Inputs(category="question"))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.question == "question"
    assert terminal_event.outputs.complaint is UNDEF
    assert terminal_event.outputs.compliment is UNDEF
    assert terminal_event.outputs.statement is UNDEF
    assert terminal_event.outputs.fallthrough is UNDEF


def test_run_workflow__complaint():
    workflow = CategoryWorkflow()

    terminal_event = workflow.run(inputs=Inputs(category="complaint"))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.question is UNDEF
    assert terminal_event.outputs.complaint == "complaint"
    assert terminal_event.outputs.compliment is UNDEF
    assert terminal_event.outputs.statement is UNDEF
    assert terminal_event.outputs.fallthrough is UNDEF


def test_run_workflow__compliment():
    workflow = CategoryWorkflow()

    terminal_event = workflow.run(inputs=Inputs(category="compliment"))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.question is UNDEF
    assert terminal_event.outputs.complaint is UNDEF
    assert terminal_event.outputs.compliment == "compliment"
    assert terminal_event.outputs.statement is UNDEF
    assert terminal_event.outputs.fallthrough is UNDEF


def test_run_workflow__statement():
    workflow = CategoryWorkflow()

    terminal_event = workflow.run(inputs=Inputs(category="statement"))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.question is UNDEF
    assert terminal_event.outputs.complaint is UNDEF
    assert terminal_event.outputs.compliment is UNDEF
    assert terminal_event.outputs.statement == "statement"
    assert terminal_event.outputs.fallthrough is UNDEF


def test_run_workflow__fallthrough():
    workflow = CategoryWorkflow()

    terminal_event = workflow.run(inputs=Inputs(category="lol"))

    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs.question is UNDEF
    assert terminal_event.outputs.complaint is UNDEF
    assert terminal_event.outputs.compliment is UNDEF
    assert terminal_event.outputs.statement is UNDEF
    assert terminal_event.outputs.fallthrough == "lol"
