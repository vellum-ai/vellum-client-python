from vellum import (
    ChatMessagePromptBlock,
    PlainTextPromptBlock,
    PromptParameters,
    RichTextPromptBlock,
    VariablePromptBlock,
)
from vellum.workflows.nodes.displayable import InlinePromptNode

from .subworkflow_node import SubworkflowNode


class PromptNode14(InlinePromptNode):
    ml_model = "gpt-4o-mini"
    blocks = [
        ChatMessagePromptBlock(
            state="ENABLED",
            cache_config=None,
            chat_role="SYSTEM",
            chat_source=None,
            chat_message_unterminated=False,
            blocks=[
                RichTextPromptBlock(
                    state="ENABLED",
                    cache_config=None,
                    blocks=[
                        PlainTextPromptBlock(
                            state="ENABLED",
                            cache_config=None,
                            text="Summarize the weather. Just use plain text, no special characters, no commas, no mathematical signs like + -",
                        )
                    ],
                )
            ],
        ),
        VariablePromptBlock(state="ENABLED", cache_config=None, input_variable="chat_history"),
    ]
    parameters = PromptParameters(
        stop=None,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        top_k=0,
        frequency_penalty=0,
        presence_penalty=0,
        logit_bias={},
        custom_parameters=None,
    )
    prompt_inputs = {"chat_history": SubworkflowNode.Outputs.chat_history}
