from abc import ABC, abstractmethod

from vellum.workflows.events.workflow import WorkflowEvent
from vellum.workflows.state.base import BaseState


class BaseWorkflowEmitter(ABC):
    @abstractmethod
    def emit_event(self, event: WorkflowEvent) -> None:
        pass

    @abstractmethod
    def snapshot_state(self, state: BaseState) -> None:
        pass
