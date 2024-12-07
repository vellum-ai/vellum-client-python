from contextlib import contextmanager
from functools import wraps
import inspect
from optparse import Option
import threading
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)

from vellum.workflows.events.types import ParentContext

ExecutionContext = Dict[str, Any]
_CONTEXT_KEY = "_execution_context"

local = threading.local()

_context_lock = threading.Lock()

F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")
P = TypeVar("P", bound=ParentContext)


def get_execution_context() -> ExecutionContext:
    """Retrieve the current execution context."""
    return getattr(local, _CONTEXT_KEY, {})


def set_execution_context(context: ExecutionContext) -> None:
    """Set the current execution context."""
    setattr(local, _CONTEXT_KEY, context)


def get_parent_context() -> ParentContext:
    return cast(ParentContext, get_execution_context().get("parent_context"))


@contextmanager
def execution_context(**kwargs: Any) -> Iterator[None]:
    """Context manager for handling execution context."""
    with _context_lock:
        prev_context = get_execution_context()
        new_context = {**prev_context, **kwargs}
        set_execution_context(new_context)
    try:
        yield
    finally:
        set_execution_context(prev_context)


# Defined set of keywords that should be extracted for the wrapper
EXECUTION_CONTEXT_ONLY_KEYWORDS: List[str] = ["parent_context"]
EXECUTION_PASSTHROUGH_KEYWORDS: List[str] = []


def wrapper_execution_context(*wrapper_args: Any, **wrapper_kwargs: Any) -> Callable[..., Any]:
    """Decorator for wrapping functions with execution context.

    Args:
        wrapper_args: Positional arguments for the wrapper context
        wrapper_kwargs: Keyword arguments for the wrapper context
    """

    def wrapper(fn: F, *_: Any, **__: Any) -> Callable[..., Any]:
        @wraps(fn)
        def wrap(*args: Any, **kwds: Any) -> Any:
            # Extract all wrapper-specific arguments from kwds
            with _context_lock:
                wrapper_specific_kwargs = {}
                fn_kwargs = kwds.copy()

                # Move all wrapper-specific keywords to wrapper_specific_kwargs
                for key in EXECUTION_CONTEXT_ONLY_KEYWORDS:
                    if key in fn_kwargs:
                        wrapper_specific_kwargs[key] = fn_kwargs.pop(key)

                temp = wrapper_specific_kwargs.pop("parent_context", None) or wrapper_kwargs.pop("parent_context", None)
                parent_context = temp or get_parent_context()

                # Combine all wrapper context
                context = {
                    "parent_context": parent_context,
                }

                if inspect.isgeneratorfunction(fn):

                    def wrapped_generator(*args: Any, **kwds: Any) -> Generator:
                        with execution_context(**context):
                            yield from fn(*args, **kwds)

                    return wrapped_generator(*args, **kwds)

            # Execute with the combined context
            with execution_context(**context):
                return fn(*args, **fn_kwargs)

        # set the wrapped methods signature to what it once was
        wrap.__signature__ = inspect.signature(fn)  # type: ignore[attr-defined]
        return wrap

    return wrapper
