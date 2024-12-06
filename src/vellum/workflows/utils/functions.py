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
    None: "null",
    type(None): "null",
}


def _compile_annotation(annotation: Any) -> dict:
    if get_origin(annotation) is Union:
        return {"anyOf": [_compile_annotation(a) for a in get_args(annotation)]}

    if get_origin(annotation) is dict:
        _, value_type = get_args(annotation)
        return {"type": "object", "additionalProperties": _compile_annotation(value_type)}

    if get_origin(annotation) is list:
        item_type = get_args(annotation)[0]
        return {"type": "array", "items": _compile_annotation(item_type)}

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
    required = []
    for param in signature.parameters.values():
        properties[param.name] = _compile_annotation(param.annotation)
        if param.default is inspect.Parameter.empty:
            required.append(param.name)
        else:
            properties[param.name]["default"] = param.default

    return FunctionDefinition(
        name=function.__name__,
        parameters={"type": "object", "properties": properties, "required": required},
    )
