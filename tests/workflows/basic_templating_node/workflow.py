from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes import TemplatingNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    city: str
    weather: str


class ExampleTemplatingNode(TemplatingNode[BaseState, str]):
    template = "The weather in {{ city }} on {{ datetime.datetime.now() }} is {{ weather }}."

    inputs = {
        "city": Inputs.city,
        "weather": Inputs.weather,
    }


class BasicTemplatingNodeWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = ExampleTemplatingNode

    class Outputs(BaseOutputs):
        result = ExampleTemplatingNode.Outputs.result
