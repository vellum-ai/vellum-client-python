import inspect
from typing import Callable

from vellum.client.types.function_definition import FunctionDefinition


def compile_function_definition(function: Callable) -> FunctionDefinition:
    """
    Converts a Python function into our Vellum-native FunctionDefinition type.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(function)
    except ValueError as e:
        raise ValueError(f"Failed to get signature for function {function.__name__}: {str(e)}")

    properties = {}
    for param in signature.parameters.values():
        property_type = type_map[param.annotation]
        properties[param.name] = {"type": property_type}

    required = [param.name for param in signature.parameters.values() if param.default is inspect.Parameter.empty]

    return FunctionDefinition(
        name=function.__name__,
        parameters={"type": "object", "properties": properties, "required": required},
    )
