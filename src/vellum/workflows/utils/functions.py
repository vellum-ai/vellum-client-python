import inspect
from typing import Any, Callable, Union, get_args, get_origin

from vellum.client.types.function_definition import FunctionDefinition

type_map = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
}


def _compile_annotation(annotation: Any) -> dict:
    if get_origin(annotation) is Union:
        return {"anyOf": [_compile_annotation(a) for a in get_args(annotation)]}

    return {"type": type_map[annotation]}


def compile_function_definition(function: Callable) -> FunctionDefinition:
    """
    Converts a Python function into our Vellum-native FunctionDefinition type.
    """

    try:
        signature = inspect.signature(function)
    except ValueError as e:
        raise ValueError(f"Failed to get signature for function {function.__name__}: {str(e)}")

    properties = {}
    for param in signature.parameters.values():
        properties[param.name] = _compile_annotation(param.annotation)

    required = [param.name for param in signature.parameters.values() if param.default is inspect.Parameter.empty]

    return FunctionDefinition(
        name=function.__name__,
        parameters={"type": "object", "properties": properties, "required": required},
    )
