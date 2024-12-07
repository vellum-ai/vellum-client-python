import dataclasses
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


def _compile_annotation(annotation: Any, defs: dict[str, Any]) -> dict:
    if get_origin(annotation) is Union:
        return {"anyOf": [_compile_annotation(a, defs) for a in get_args(annotation)]}

    if get_origin(annotation) is dict:
        _, value_type = get_args(annotation)
        return {"type": "object", "additionalProperties": _compile_annotation(value_type, defs)}

    if get_origin(annotation) is list:
        item_type = get_args(annotation)[0]
        return {"type": "array", "items": _compile_annotation(item_type, defs)}

    if dataclasses.is_dataclass(annotation):
        if annotation.__name__ not in defs:
            properties = {}
            required = []
            for field in dataclasses.fields(annotation):
                properties[field.name] = _compile_annotation(field.type, defs)
                if field.default is dataclasses.MISSING:
                    required.append(field.name)
                else:
                    properties[field.name]["default"] = field.default
            defs[annotation.__name__] = {"type": "object", "properties": properties, "required": required}
        return {"$ref": f"#/$defs/{annotation.__name__}"}

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
    defs: dict[str, Any] = {}
    for param in signature.parameters.values():
        properties[param.name] = _compile_annotation(param.annotation, defs)
        if param.default is inspect.Parameter.empty:
            required.append(param.name)
        else:
            properties[param.name]["default"] = param.default

    parameters = {"type": "object", "properties": properties, "required": required}
    if defs:
        parameters["$defs"] = defs

    return FunctionDefinition(
        name=function.__name__,
        parameters=parameters,
    )
