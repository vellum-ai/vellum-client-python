from vellum.workflows.nodes.displayable import ConditionalNode as BaseConditionalNode
from vellum.workflows.ports import Port

from .templating_node import BaseTemplatingNode


class ConditionalNode(BaseConditionalNode):
    class Ports(BaseConditionalNode.Ports):
        branch_8 = Port.on_if(result.equals("weather"))
        branch_9 = Port.on_elif(result.equals("flight status"))
        branch_10 = Port.on_elif(result.equals("faa"))
        branch_11 = Port.on_else()
