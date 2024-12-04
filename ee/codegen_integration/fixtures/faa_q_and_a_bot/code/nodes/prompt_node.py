from vellum import (
    ChatMessagePromptBlock,
    PlainTextPromptBlock,
    PromptParameters,
    RichTextPromptBlock,
    VariablePromptBlock,
)
from vellum.workflows.nodes.displayable import InlinePromptNode

from .most_recent_message import MostRecentMessage


class PromptNode(InlinePromptNode):
    ml_model = "gpt-4o"
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
                            text='You are an expert classifier. You will analyze the chat and output one of the following in JSON format: \n\n1. "weather" if it is a question about the weather\n2. "flight status" if it is about which flights are currently in transit at a certain airport\n3. "faa" if the question is about any FAA related aviation policies\n4. "other" if the question is about anything else',
                        )
                    ],
                )
            ],
        ),
        ChatMessagePromptBlock(
            state="ENABLED",
            cache_config=None,
            chat_role="USER",
            chat_source=None,
            chat_message_unterminated=False,
            blocks=[
                RichTextPromptBlock(
                    state="ENABLED",
                    cache_config=None,
                    blocks=[
                        VariablePromptBlock(
                            state="ENABLED", cache_config=None, input_variable="var_1"
                        )
                    ],
                )
            ],
        ),
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
        custom_parameters={
            "json_mode": True,
            "json_schema": {
                "name": "Classification",
                "schema": {
                    "type": "object",
                    "required": ["classification"],
                    "properties": {
                        "classification": {"type": "string", "description": ""}
                    },
                },
            },
        },
    )
    prompt_inputs = {"var_1": MostRecentMessage.Outputs.result}
