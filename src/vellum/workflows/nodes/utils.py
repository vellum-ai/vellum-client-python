from functools import cache
from typing import Type

from vellum.workflows.nodes import BaseNode
from vellum.workflows.types.generics import NodeType

ADORNMENT_MODULE_NAME = "<adornment>"


@cache
def get_wrapped_node(node: Type[NodeType]) -> Type[BaseNode]:
    wrapped_node = getattr(node, "__wrapped_node__", None)
    if wrapped_node is None:
        raise AttributeError("Wrapped node not found")

    return wrapped_node


def has_wrapped_node(node: Type[NodeType]) -> bool:
    try:
        get_wrapped_node(node)
    except AttributeError:
        return False

    return True
