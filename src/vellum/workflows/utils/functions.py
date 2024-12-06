from typing import Callable

from vellum.client.types.function_definition import FunctionDefinition


def compile_function_definition(function: Callable) -> FunctionDefinition:
    """
    Converts a Python function into our Vellum-native FunctionDefinition type.
    """

    return FunctionDefinition(
        name=function.__name__,
    )
