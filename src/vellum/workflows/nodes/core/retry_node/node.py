from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Optional, Type

from vellum.workflows.errors.types import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.bases.base import BaseNodeMeta
from vellum.workflows.state.base import BaseState
from vellum.workflows.types.generics import StateType

if TYPE_CHECKING:
    from vellum.workflows import BaseWorkflow


class _RetryNodeMeta(BaseNodeMeta):
    @property
    def _localns(cls) -> Dict[str, Any]:
        return {
            **super()._localns,
            "SubworkflowInputs": getattr(cls, "SubworkflowInputs"),
        }


class RetryNode(BaseNode[StateType], Generic[StateType], metaclass=_RetryNodeMeta):
    """
    Used to retry a Subworkflow a specified number of times.

    max_attempts: int - The maximum number of attempts to retry the Subworkflow
    retry_on_error_code: Optional[VellumErrorCode] = None - The error code to retry on
    subworkflow: Type["BaseWorkflow[SubworkflowInputs, BaseState]"] - The Subworkflow to execute
    """

    max_attempts: int
    retry_on_error_code: Optional[WorkflowErrorCode] = None
    subworkflow: Type["BaseWorkflow[SubworkflowInputs, BaseState]"]

    class SubworkflowInputs(BaseInputs):
        attempt_number: int

    def run(self) -> BaseNode.Outputs:
        last_exception = Exception("max_attempts must be greater than 0")
        for index in range(self.max_attempts):
            attempt_number = index + 1
            subworkflow = self.subworkflow(
                parent_state=self.state,
                context=self._context,
            )
            terminal_event = subworkflow.run(
                inputs=self.SubworkflowInputs(attempt_number=attempt_number),
            )
            if terminal_event.name == "workflow.execution.fulfilled":
                node_outputs = self.Outputs()
                workflow_output_vars = vars(terminal_event.outputs)

                for output_name in workflow_output_vars:
                    setattr(node_outputs, output_name, workflow_output_vars[output_name])

                return node_outputs
            elif terminal_event.name == "workflow.execution.paused":
                last_exception = NodeException(
                    code=WorkflowErrorCode.INVALID_OUTPUTS,
                    message=f"Subworkflow unexpectedly paused on attempt {attempt_number}",
                )
                break
            elif self.retry_on_error_code and self.retry_on_error_code != terminal_event.error.code:
                last_exception = NodeException(
                    code=WorkflowErrorCode.INVALID_OUTPUTS,
                    message=f"""Unexpected rejection on attempt {attempt_number}: {terminal_event.error.code.value}.
Message: {terminal_event.error.message}""",
                )
                break
            else:
                last_exception = Exception(terminal_event.error.message)

        raise last_exception

    @classmethod
    def wrap(
        cls, max_attempts: int, retry_on_error_code: Optional[WorkflowErrorCode] = None
    ) -> Callable[..., Type["RetryNode"]]:
        _max_attempts = max_attempts
        _retry_on_error_code = retry_on_error_code

        def decorator(inner_cls: Type[BaseNode]) -> Type["RetryNode"]:
            # Investigate how to use dependency injection to avoid circular imports
            # https://app.shortcut.com/vellum/story/4116
            from vellum.workflows import BaseWorkflow

            class Subworkflow(BaseWorkflow[RetryNode.SubworkflowInputs, BaseState]):
                graph = inner_cls

                # mypy is wrong here, this works and is defined
                class Outputs(inner_cls.Outputs):  # type: ignore[name-defined]
                    pass

            class WrappedNode(RetryNode[StateType]):
                max_attempts = _max_attempts
                retry_on_error_code = _retry_on_error_code

                subworkflow = Subworkflow

                class Outputs(Subworkflow.Outputs):
                    pass

            return WrappedNode

        return decorator
