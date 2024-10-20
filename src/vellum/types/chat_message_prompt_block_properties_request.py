# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .chat_message_role import ChatMessageRole
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class ChatMessagePromptBlockPropertiesRequest(UniversalBaseModel):
    """
    The properties of a ChatMessagePromptTemplateBlock
    """

    blocks: typing.List["PromptBlockRequest"]
    chat_role: typing.Optional[ChatMessageRole] = None
    chat_source: typing.Optional[str] = None
    chat_message_unterminated: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .chat_message_prompt_block_request import ChatMessagePromptBlockRequest  # noqa: E402
from .prompt_block_request import PromptBlockRequest  # noqa: E402

update_forward_refs(
    ChatMessagePromptBlockRequest, ChatMessagePromptBlockPropertiesRequest=ChatMessagePromptBlockPropertiesRequest
)
update_forward_refs(ChatMessagePromptBlockPropertiesRequest)
