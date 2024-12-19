from vellum.workflows.errors.types import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core import ErrorNode
from vellum.workflows.nodes.core.try_node.node import TryNode
from vellum.workflows.ports.port import Port
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    threshold: int


@TryNode.wrap()
class StartNode(BaseNode):
    arg = Inputs.threshold

    class Outputs(BaseNode.Outputs):
        value: int

    def run(self) -> Outputs:
        if self.arg < 5:
            raise NodeException(message="This is a flaky node", code=WorkflowErrorCode.INVALID_OUTPUTS)
        return self.Outputs(value=self.arg)


class RouterNode(BaseNode):
    class Ports(BaseNode.Ports):
        success = Port.on_if(StartNode.Outputs.error.is_null())
        fail = Port.on_else()


class SuccessNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = StartNode.Outputs.value


class FailNode(ErrorNode):
    error = StartNode.Outputs.error


class ErrorWithTryWorkflow(BaseWorkflow[Inputs, BaseState]):
    """
    A simple workflow that an ErrorNode could use the error
    output from a TryNode.
    """

    graph = StartNode >> {
        RouterNode.Ports.success >> SuccessNode,
        RouterNode.Ports.fail >> FailNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        final_value = SuccessNode.Outputs.result
