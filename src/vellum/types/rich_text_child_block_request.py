# This file was auto-generated by Fern from our API Definition.

import typing
from .variable_prompt_block_request import VariablePromptBlockRequest
from .plain_text_prompt_block_request import PlainTextPromptBlockRequest

RichTextChildBlockRequest = typing.Union[VariablePromptBlockRequest, PlainTextPromptBlockRequest]