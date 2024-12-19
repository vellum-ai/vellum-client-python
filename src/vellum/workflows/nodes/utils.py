from functools import cache
from typing import Type

from vellum.workflows.nodes import BaseNode
from vellum.workflows.types.generics import NodeType

ADORNMENT_MODULE_NAME = "<adornment>"


def get_unadorned_node(node: Type[NodeType]) -> Type[BaseNode]:
    if has_wrapped_node(node):
        return get_unadorned_node(get_wrapped_node(node))

    return node


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
