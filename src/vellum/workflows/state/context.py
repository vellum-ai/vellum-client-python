from functools import cached_property
from queue import Queue
from typing import TYPE_CHECKING, Optional

from vellum import Vellum
from vellum.workflows.vellum_client import create_vellum_client

if TYPE_CHECKING:
    from vellum.workflows.events.workflow import WorkflowEvent


class WorkflowContext:
    def __init__(self, _vellum_client: Optional[Vellum] = None):
        self._vellum_client = _vellum_client
        self._event_queue: Optional[Queue["WorkflowEvent"]] = None

    @cached_property
    def vellum_client(self) -> Vellum:
        if self._vellum_client:
            return self._vellum_client

        return create_vellum_client()

    def _emit_subworkflow_event(self, event: "WorkflowEvent") -> None:
        if self._event_queue:
            self._event_queue.put(event)

    def _register_event_queue(self, event_queue: Queue["WorkflowEvent"]) -> None:
        self._event_queue = event_queue
