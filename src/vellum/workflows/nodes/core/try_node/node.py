from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Optional, Tuple, Type, TypeVar

from vellum.workflows.errors.types import VellumError, VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.bases.base import BaseNodeMeta
from vellum.workflows.outputs.base import BaseOutputs
from vellum.workflows.types.generics import StateType

if TYPE_CHECKING:
    from vellum.workflows import BaseWorkflow

Subworkflow = Type["BaseWorkflow"]
_T = TypeVar("_T", bound=BaseOutputs)


class _TryNodeMeta(BaseNodeMeta):
    def __new__(cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]) -> Any:
        node_class = super().__new__(cls, name, bases, dct)

        subworkflow_attribute = dct.get("subworkflow")
        if not subworkflow_attribute:
            return node_class

        subworkflow_outputs = getattr(subworkflow_attribute, "Outputs")
        if not issubclass(subworkflow_outputs, BaseOutputs):
            raise ValueError("subworkflow.Outputs must be a subclass of BaseOutputs")

        outputs_class = dct.get("Outputs")
        if not outputs_class:
            raise ValueError("Outputs class not found in base classes")

        if not issubclass(outputs_class, BaseNode.Outputs):
            raise ValueError("Outputs class must be a subclass of BaseNode.Outputs")

        for descriptor in subworkflow_outputs:
            if descriptor.name == "error":
                raise ValueError("`error` is a reserved name for TryNode.Outputs")

            setattr(outputs_class, descriptor.name, descriptor)

        return node_class


class TryNode(BaseNode[StateType], Generic[StateType], metaclass=_TryNodeMeta):
    """
    Used to execute a Subworkflow and handle errors.

    on_error_code: Optional[VellumErrorCode] = None - The error code to handle
    subworkflow: Type["BaseWorkflow"] - The Subworkflow to execute
    """

    on_error_code: Optional[VellumErrorCode] = None
    subworkflow: Type["BaseWorkflow"]

    class Outputs(BaseNode.Outputs):
        error: Optional[VellumError] = None

    def run(self) -> Outputs:
        subworkflow = self.subworkflow(
            parent_state=self.state,
        )
        terminal_event = subworkflow.run()

        if terminal_event.name == "workflow.execution.fulfilled":
            outputs = self.Outputs()
            for descriptor, value in terminal_event.outputs:
                setattr(outputs, descriptor.name, value)
            return outputs
        elif terminal_event.name == "workflow.execution.paused":
            raise NodeException(
                code=VellumErrorCode.INVALID_OUTPUTS,
                message="Subworkflow unexpectedly paused within Try Node",
            )
        elif self.on_error_code and self.on_error_code != terminal_event.error.code:
            raise NodeException(
                code=VellumErrorCode.INVALID_OUTPUTS,
                message=f"""Unexpected rejection: {terminal_event.error.code.value}.
Message: {terminal_event.error.message}""",
            )
        else:
            return self.Outputs(
                error=terminal_event.error,
            )

    @classmethod
    def wrap(cls, on_error_code: Optional[VellumErrorCode] = None) -> Callable[..., Type["TryNode"]]:
        _on_error_code = on_error_code

        def decorator(inner_cls: Type[BaseNode]) -> Type["TryNode"]:
            # Investigate how to use dependency injection to avoid circular imports
            # https://app.shortcut.com/vellum/story/4116
            from vellum.workflows import BaseWorkflow

            class Subworkflow(BaseWorkflow):
                inner_cls._is_wrapped_node = True
                graph = inner_cls

                # mypy is wrong here, this works and is defined
                class Outputs(inner_cls.Outputs):  # type: ignore[name-defined]
                    pass

            class WrappedNode(TryNode[StateType]):
                on_error_code = _on_error_code

                subworkflow = Subworkflow

            return WrappedNode

        return decorator
