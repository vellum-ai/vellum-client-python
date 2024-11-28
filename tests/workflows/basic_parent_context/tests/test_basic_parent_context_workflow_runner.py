from vellum.workflows.events import WorkflowEventType
from vellum.workflows.events.types import WorkflowParentContext

from tests.workflows.basic_parent_context.basic_workflow import TrivialWorkflow


def test_run_workflow__happy_path():
    workflow = TrivialWorkflow()
    terminal_event = workflow.run()

    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.parent == None


def test_stream_workflow__happy_path():
    workflow = TrivialWorkflow()
    events = list(workflow.stream(event_types={WorkflowEventType.WORKFLOW, WorkflowEventType.NODE}))

    assert len(events) == 4

    assert events[0].name == "workflow.execution.initiated"
    assert events[0].parent is None

    assert events[1].name == "node.execution.initiated"
    assert type(events[1].parent) == type(WorkflowParentContext)
    assert events[1].parent.workflow_definition == workflow.__class__

    assert events[-1].name == "workflow.execution.fulfilled"
    assert events[-1].parent is None
