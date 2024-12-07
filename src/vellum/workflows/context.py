from contextlib import contextmanager
from functools import wraps
import inspect
from optparse import Option
import threading
from typing import (
    Any,
    Callable,
    Dict,
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
    prev_context = get_execution_context()
    try:
        set_execution_context({**prev_context, **kwargs})
        yield
    finally:
        set_execution_context(prev_context)


# Defined set of keywords that should be extracted for the wrapper
EXECUTION_CONTEXT_ONLY_KEYWORDS: List[str] = ["context", "parent_context", "execution_id"]
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
            wrapper_specific_kwargs = {}
            fn_kwargs = kwds.copy()

            # Move all wrapper-specific keywords to wrapper_specific_kwargs
            for key in EXECUTION_CONTEXT_ONLY_KEYWORDS:
                if key in fn_kwargs:
                    wrapper_specific_kwargs[key] = fn_kwargs.pop(key)

            parent_context = get_parent_context()
            if wrapper_specific_kwargs.get("parent_context") or wrapper_kwargs.get("parent_context"):
                temp = wrapper_specific_kwargs.pop("parent_context", None) or wrapper_kwargs.pop("parent_context", None)
                if temp:
                    parent_context = temp

            # Combine all wrapper context
            context = {
                **wrapper_kwargs,  # Context from decorator
                **wrapper_specific_kwargs,  # Context from function call
                "parent_context": parent_context,
            }

            # Execute with the combined context
            with execution_context(**context):
                return fn(*args, **fn_kwargs)

        # set the wrapped methods signature to what it once was
        wrap.__signature__ = inspect.signature(fn)  # type: ignore[attr-defined]
        return wrap

    return wrapper


class ExecutionContextMixin:
    def _wrap_method(self, method: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap a method with execution context."""

        # Get the parent context from the current execution context
        prev_context = get_execution_context()

        # Use your existing wrapper with the parent context
        wrapped = wrapper_execution_context(**prev_context)(method)

        return wrapped

    def __getattribute__(self, name: str) -> Any:
        """Wrap methods with execution context when they're accessed."""
        attr = object.__getattribute__(self, name)
        if callable(attr) and not name.startswith("__"):  # Debug
            wrap_method = object.__getattribute__(self, "_wrap_method")
            return wrap_method(attr)
        return attr
