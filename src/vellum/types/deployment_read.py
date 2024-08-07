# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .entity_status import EntityStatus
from .environment_enum import EnvironmentEnum
from .vellum_variable import VellumVariable


class DeploymentRead(pydantic_v1.BaseModel):
    id: str
    created: dt.datetime
    label: str = pydantic_v1.Field()
    """
    A human-readable label for the deployment
    """

    name: str = pydantic_v1.Field()
    """
    A name that uniquely identifies this deployment within its workspace
    """

    status: typing.Optional[EntityStatus] = pydantic_v1.Field(default=None)
    """
    The current status of the deployment
    
    - `ACTIVE` - Active
    - `ARCHIVED` - Archived
    """

    environment: typing.Optional[EnvironmentEnum] = pydantic_v1.Field(default=None)
    """
    The environment this deployment is used in
    
    - `DEVELOPMENT` - Development
    - `STAGING` - Staging
    - `PRODUCTION` - Production
    """

    last_deployed_on: dt.datetime
    input_variables: typing.List[VellumVariable]
    description: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    A human-readable description of the deployment
    """

    active_model_version_ids: typing.List[str] = pydantic_v1.Field()
    """
    Deprecated. The Prompt execution endpoints return a `prompt_version_id` that could be used instead.
    """

    last_deployed_history_item_id: str = pydantic_v1.Field()
    """
    The ID of the history item associated with this Deployment's LATEST Release Tag
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
