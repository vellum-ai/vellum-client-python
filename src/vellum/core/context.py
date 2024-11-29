from contextlib import contextmanager
from functools import wraps
import inspect
import threading
from typing import Any, Callable, Dict, Iterator, TypeVar, Union, cast

from vellum.workflows.events.types import ParentContext

LoggingContext = Dict[str, Any]
_CONTEXT_KEY = "_execution_context"

local = threading.local()

F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')
P = TypeVar('P', bound=ParentContext)


def get_execution_context() -> LoggingContext:
    """Retrieve the current execution context."""
    return getattr(local, _CONTEXT_KEY, {})


def set_execution_context(context: LoggingContext) -> None:
    """Set the current execution context."""
    setattr(local, _CONTEXT_KEY, context)


@contextmanager
def execution_context(**kwargs: Any) -> Iterator[None]:
    """Context manager for handling execution context."""
    prev_context = get_execution_context()
    try:
        set_execution_context({**prev_context, **kwargs})
        yield
    finally:
        set_execution_context(prev_context)


def wrapper_execution_parent_context(
        context: Union[ParentContext, Callable[[Any], ParentContext]],
        **kwargs: Any
) -> Callable[[F], F]:
    """Decorator for wrapping functions with execution context.
    
    Args:
        context: Either a context object or a function that creates one
        kwargs: Additional context parameters
    """

    def wrapper(fn: F) -> F:
        @wraps(fn)
        def wrap(*args: Any, **kwds: Any) -> Any:
            prev_context = get_execution_context()
            prev_parent_context = prev_context.get('parent_context')

            # Check if this is a class method with a context factory
            first_param = next(iter(inspect.signature(fn).parameters), None)
            is_method = first_param in ('self', 'cls')
            has_instance = bool(args)
            is_context_factory = callable(context)

            # Create the appropriate context
            if is_method and has_instance and is_context_factory:
                instance = args[0]
                # new_context = cast(Callable[[Any], ParentContext], context)(instance)
                new_context = context(instance)  # type: ignore
            else:
                # new_context = cast(ParentContext, context)
                new_context = context  # type: ignore

            # Chain the parent context
            if prev_parent_context is not None:
                new_context.parent = prev_parent_context

            # Execute with the new context
            with execution_context(parent_context=new_context, **kwargs):
                return fn(*args, **kwds)

        return cast(F, wrap)

    return wrapper
