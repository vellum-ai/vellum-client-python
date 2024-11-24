from functools import cached_property
from typing import Optional

from vellum import Vellum

from vellum.workflows.vellum_client import create_vellum_client


class WorkflowContext:
    def __init__(self, _vellum_client: Optional[Vellum] = None):
        self._vellum_client = _vellum_client

    @cached_property
    def vellum_client(self) -> Vellum:
        if self._vellum_client:
            return self._vellum_client

        return create_vellum_client()
