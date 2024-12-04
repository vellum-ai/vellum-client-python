from vellum import (
    ChatMessagePromptBlock,
    PlainTextPromptBlock,
    PromptParameters,
    RichTextPromptBlock,
    VariablePromptBlock,
)
from vellum.workflows.nodes.displayable import InlinePromptNode

from .most_recent_message import MostRecentMessage


class PromptNode16(InlinePromptNode):
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
                            text='Respond with the IATA airport name this incoming message is about. For example, respond only with "SJC", "SFO", "EWR" or "JFK"\n\n',
                        ),
                        VariablePromptBlock(state="ENABLED", cache_config=None, input_variable="most_recent_message"),
                    ],
                )
            ],
        )
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
    prompt_inputs = {"most_recent_message": MostRecentMessage.Outputs.result}