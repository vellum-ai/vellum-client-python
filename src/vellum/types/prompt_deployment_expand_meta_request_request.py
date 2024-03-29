# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class PromptDeploymentExpandMetaRequestRequest(pydantic.BaseModel):
    model_name: typing.Optional[bool] = pydantic.Field(
        description="If enabled, the response will include the model identifier representing the ML Model invoked by the Prompt Deployment."
    )
    latency: typing.Optional[bool] = pydantic.Field(
        description="If enabled, the response will include the time in nanoseconds it took to execute the Prompt Deployment."
    )
    deployment_release_tag: typing.Optional[bool] = pydantic.Field(
        description="If enabled, the response will include the release tag of the Prompt Deployment."
    )
    prompt_version_id: typing.Optional[bool] = pydantic.Field(
        description="If enabled, the response will include the ID of the Prompt Version backing the deployment."
    )
    finish_reason: typing.Optional[bool] = pydantic.Field(
        description="If enabled, the response will include the reason provided by the model for why the execution finished."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
