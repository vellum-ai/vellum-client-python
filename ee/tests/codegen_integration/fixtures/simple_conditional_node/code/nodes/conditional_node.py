from vellum.workflows.nodes.displayable import ConditionalNode as BaseConditionalNode
from vellum.workflows.ports import Port

from ..inputs import Inputs


class ConditionalNode(BaseConditionalNode):
    class Ports(BaseConditionalNode.Ports):
        branch_1 = Port.on_if(Inputs.foobar.equals("Hello World!"))
        branch_2 = Port.on_elif(Inputs.bazbaz.equals("testing"))
        branch_3 = Port.on_else()
