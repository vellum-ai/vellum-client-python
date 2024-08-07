# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .document_document_to_document_index import DocumentDocumentToDocumentIndex
from .document_status import DocumentStatus
from .processing_state_enum import ProcessingStateEnum


class DocumentRead(pydantic_v1.BaseModel):
    id: str
    external_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The unique id of this document as it exists in the user's system.
    """

    last_uploaded_at: dt.datetime
    label: str = pydantic_v1.Field()
    """
    A human-readable label for the document. Defaults to the originally uploaded file's file name.
    """

    processing_state: typing.Optional[ProcessingStateEnum] = pydantic_v1.Field(default=None)
    """
    The current processing state of the document
    
    - `QUEUED` - Queued
    - `PROCESSING` - Processing
    - `PROCESSED` - Processed
    - `FAILED` - Failed
    """

    status: typing.Optional[DocumentStatus] = pydantic_v1.Field(default=None)
    """
    The current status of the document
    
    - `ACTIVE` - Active
    """

    original_file_url: typing.Optional[str] = None
    processed_file_url: typing.Optional[str] = None
    document_to_document_indexes: typing.List[DocumentDocumentToDocumentIndex]
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    A previously supplied JSON object containing metadata that can be filtered on when searching.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
