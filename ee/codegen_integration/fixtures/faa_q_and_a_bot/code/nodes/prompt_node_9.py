from vellum import (
    ChatMessagePromptBlock,
    PlainTextPromptBlock,
    PromptParameters,
    RichTextPromptBlock,
    VariablePromptBlock,
)
from vellum.workflows.nodes.displayable import InlinePromptNode

from .formatted_search_results import FormattedSearchResults
from .most_recent_message import MostRecentMessage


class PromptNode9(InlinePromptNode):
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
                            text=" Question:\n---------------\n",
                        ),
                        VariablePromptBlock(
                            state="ENABLED",
                            cache_config=None,
                            input_variable="question",
                        ),
                        PlainTextPromptBlock(
                            state="ENABLED",
                            cache_config=None,
                            text="\n\nPolicy Quotes:\n-----------------------\n",
                        ),
                        VariablePromptBlock(state="ENABLED", cache_config=None, input_variable="context"),
                    ],
                ),
                RichTextPromptBlock(
                    state="ENABLED",
                    cache_config=None,
                    blocks=[
                        PlainTextPromptBlock(
                            state="ENABLED",
                            cache_config=None,
                            text="You are an expert on FAA rules, guidelines, and safety. Answer the above question given the context. Provide citation of the policy you got it from at the end of the response. If you don't know the answer, say \"Sorry, I don't know\"\n\nLimit your response to 250 words. Just use plain text, no special characters, no commas, no mathematical signs like + -",
                        )
                    ],
                ),
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
    prompt_inputs = {
        "question": MostRecentMessage.Outputs.result,
        "context": FormattedSearchResults.Outputs.result,
    }
