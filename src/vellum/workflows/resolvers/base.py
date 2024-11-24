from abc import ABC, abstractmethod
from typing import Iterator

from vellum.workflows.events.workflow import WorkflowEvent
from vellum.workflows.state.base import BaseState


class BaseWorkflowResolver(ABC):
    @abstractmethod
    def get_latest_execution_events(self) -> Iterator[WorkflowEvent]:
        pass

    @abstractmethod
    def get_state_snapshot_history(self) -> Iterator[BaseState]:
        pass
