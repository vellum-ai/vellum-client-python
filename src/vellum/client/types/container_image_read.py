# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .entity_visibility import EntityVisibility
import datetime as dt
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ContainerImageRead(UniversalBaseModel):
    id: str
    name: str
    visibility: EntityVisibility
    created: dt.datetime
    modified: dt.datetime
    repository: str
    sha: str
    tags: typing.List[str]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
