from functools import cached_property
from typing import Optional

from vellum import Vellum
from vellum.workflows.events.types import ParentContext
from vellum.workflows.vellum_client import create_vellum_client


class WorkflowContext:
    def __init__(
        self,
        _vellum_client: Optional[Vellum] = None,
        _parent_context: Optional["ParentContext"] = None,
    ):
        self._vellum_client = _vellum_client
        self._parent_context = _parent_context

    @cached_property
    def vellum_client(self) -> Vellum:
        if self._vellum_client:
            return self._vellum_client

        return create_vellum_client()

    @cached_property
    def parent_context(self) -> Optional["ParentContext"]:
        if self._parent_context:
            return self._parent_context
        return None
