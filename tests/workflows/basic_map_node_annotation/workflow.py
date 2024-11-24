from typing import List

from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes import MapNode
from vellum.workflows.nodes.bases import BaseNode


class Inputs(BaseInputs):
    fruits: List[str]


@MapNode.wrap(items=Inputs.fruits)
class MappableNode(BaseNode):
    item = MapNode.SubworkflowInputs.item
    index = MapNode.SubworkflowInputs.index

    class Outputs(BaseNode.Outputs):
        count: int

    def run(self) -> Outputs:
        return self.Outputs(count=len(self.item) + self.index)


class SimpleMapExample(BaseWorkflow):
    graph = MappableNode

    class Outputs(BaseWorkflow.Outputs):
        # TODO: We'll need to infer the type T of Subworkflow.Outputs[name] so we could do List[T] here
        # https://app.shortcut.com/vellum/story/4119
        # final_value: List[int] = MappableNode.Outputs.count
        final_value = MappableNode.Outputs.count
