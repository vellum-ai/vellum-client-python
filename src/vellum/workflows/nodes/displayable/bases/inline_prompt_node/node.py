from uuid import uuid4
from typing import ClassVar, Generic, Iterator, List, Optional, Tuple, cast

from vellum import (
    AdHocExecutePromptEvent,
    AdHocExpandMeta,
    ChatMessage,
    FunctionDefinition,
    PromptBlock,
    PromptParameters,
    PromptRequestChatHistoryInput,
    PromptRequestInput,
    PromptRequestJsonInput,
    PromptRequestStringInput,
    VellumVariable,
)
from vellum.workflows.constants import OMIT
from vellum.workflows.context import get_parent_context
from vellum.workflows.errors import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.displayable.bases.base_prompt_node import BasePromptNode
from vellum.workflows.nodes.displayable.bases.inline_prompt_node.constants import DEFAULT_PROMPT_PARAMETERS
from vellum.workflows.types.generics import StateType


class BaseInlinePromptNode(BasePromptNode, Generic[StateType]):
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

    ml_model: ClassVar[str]

    # The blocks that make up the Prompt
    blocks: ClassVar[List[PromptBlock]]

    # The functions/tools that a Prompt has access to
    functions: Optional[List[FunctionDefinition]] = OMIT

    parameters: PromptParameters = DEFAULT_PROMPT_PARAMETERS
    expand_meta: Optional[AdHocExpandMeta] = OMIT

    def _get_prompt_event_stream(self) -> Iterator[AdHocExecutePromptEvent]:
        input_variables, input_values = self._compile_prompt_inputs()
        parent_context = get_parent_context() or self._context.parent_context

        return self._context.vellum_client.ad_hoc.adhoc_execute_prompt_stream(
            ml_model=self.ml_model,
            input_values=input_values,
            input_variables=input_variables,
            parameters=self.parameters,
            blocks=self.blocks,
            functions=self.functions,
            expand_meta=self.expand_meta,
            request_options=self.request_options,
            execution_context={"parent_context": parent_context.model_dump() if parent_context else None},
        )

    def _compile_prompt_inputs(self) -> Tuple[List[VellumVariable], List[PromptRequestInput]]:
        input_variables: List[VellumVariable] = []
        input_values: List[PromptRequestInput] = []

        for input_name, input_value in self.prompt_inputs.items():
            if isinstance(input_value, str):
                input_variables.append(
                    VellumVariable(
                        # TODO: Determine whether or not we actually need an id here and if we do,
                        #   figure out how to maintain stable id references.
                        #   https://app.shortcut.com/vellum/story/4080
                        id=str(uuid4()),
                        key=input_name,
                        type="STRING",
                    )
                )
                input_values.append(
                    PromptRequestStringInput(
                        key=input_name,
                        value=input_value,
                    )
                )
            elif isinstance(input_value, list) and all(isinstance(message, ChatMessage) for message in input_value):
                input_variables.append(
                    VellumVariable(
                        # TODO: Determine whether or not we actually need an id here and if we do,
                        #   figure out how to maintain stable id references.
                        #   https://app.shortcut.com/vellum/story/4080
                        id=str(uuid4()),
                        key=input_name,
                        type="CHAT_HISTORY",
                    )
                )
                input_values.append(
                    PromptRequestChatHistoryInput(
                        key=input_name,
                        value=cast(List[ChatMessage], input_value),
                    )
                )
            elif isinstance(input_value, dict):
                # Note: We may want to fail early here if we know that input_value is not
                #   JSON serializable.
                input_values.append(
                    PromptRequestJsonInput(
                        key=input_name,
                        value=input_value,
                    )
                )
            else:
                raise NodeException(
                    message=f"Unrecognized input type for input '{input_name}': {input_value.__class__}",
                    code=VellumErrorCode.INVALID_INPUTS,
                )

        return input_variables, input_values
