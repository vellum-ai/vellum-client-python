from vellum.workflows import BaseWorkflow
from vellum.workflows.errors import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode


class RejectedNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        pass

    def run(self) -> Outputs:
        raise NodeException(code=WorkflowErrorCode.USER_DEFINED_ERROR, message="Node was rejected")


class BasicRejectedWorkflow(BaseWorkflow):
    graph = RejectedNode
