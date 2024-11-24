from vellum.workflows.events.workflow import WorkflowEvent


def is_terminal_event(event: WorkflowEvent) -> bool:
    return event.name in {"workflow.execution.fulfilled", "workflow.execution.rejected", "workflow.execution.paused"}
