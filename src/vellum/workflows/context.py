from contextlib import contextmanager
import threading
from typing import Iterator, Optional, cast

from vellum.client.core import UniversalBaseModel
from vellum.workflows.events.types import ParentContext


class ExecutionContext(UniversalBaseModel):
    parent_context: Optional[ParentContext] = None


_CONTEXT_KEY = "_execution_context"

local = threading.local()


def get_execution_context() -> ExecutionContext:
    """Retrieve the current execution context."""
    return getattr(local, _CONTEXT_KEY, ExecutionContext())


def set_execution_context(context: ExecutionContext) -> None:
    """Set the current execution context."""
    setattr(local, _CONTEXT_KEY, context)


def get_parent_context() -> ParentContext:
    return cast(ParentContext, get_execution_context().parent_context)


@contextmanager
def execution_context(parent_context: Optional[ParentContext] = None) -> Iterator[None]:
    """Context manager for handling execution context."""
    prev_context = get_execution_context()
    set_context = ExecutionContext(parent_context=parent_context) if parent_context else prev_context

    try:
        set_execution_context(set_context)
        yield
    finally:
        set_execution_context(prev_context)
