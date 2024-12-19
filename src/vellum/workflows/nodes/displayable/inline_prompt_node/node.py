from typing import Iterator

from vellum.workflows.errors import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.displayable.bases import BaseInlinePromptNode as BaseInlinePromptNode
from vellum.workflows.outputs import BaseOutput
from vellum.workflows.types.generics import StateType


class InlinePromptNode(BaseInlinePromptNode[StateType]):
    """
    Used to execute a Prompt defined inline.

    prompt_inputs: EntityInputsInterface - The inputs for the Prompt
    ml_model: str - Either the ML Model's UUID or its name.
    blocks: List[PromptBlock] - The blocks that make up the Prompt
    functions: Optional[List[FunctionDefinition]] - The functions to include in the Prompt
    parameters: PromptParameters - The parameters for the Prompt
    expand_meta: Optional[AdHocExpandMeta] - Expandable execution fields to include in the response
    request_options: Optional[RequestOptions] - The request options to use for the Prompt Execution
    """

    class Outputs(BaseInlinePromptNode.Outputs):
        """
        The outputs of the InlinePromptNode.

        text: str - The result of the Prompt Execution
        """

        text: str

    def run(self) -> Iterator[BaseOutput]:
        outputs = yield from self._process_prompt_event_stream()
        if not outputs:
            raise NodeException(
                message="Expected to receive outputs from Prompt",
                code=WorkflowErrorCode.INTERNAL_ERROR,
            )

        string_output = next((output for output in outputs if output.type == "STRING"), None)
        if not string_output or string_output.value is None:
            output_types = {output.type for output in outputs}
            is_plural = len(output_types) > 1
            raise NodeException(
                message=f"Expected to receive a non-null string output from Prompt. Only found outputs of type{'s' if is_plural else ''}: {', '.join(output_types)}",  # noqa: E501
                code=WorkflowErrorCode.INTERNAL_ERROR,
            )

        yield BaseOutput(name="text", value=string_output.value)
