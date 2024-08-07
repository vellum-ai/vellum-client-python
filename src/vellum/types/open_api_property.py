# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class OpenApiProperty_Array(pydantic_v1.BaseModel):
    min_items: typing.Optional[int] = None
    max_items: typing.Optional[int] = None
    unique_items: typing.Optional[bool] = None
    items: OpenApiProperty
    prefix_items: typing.Optional[typing.List[OpenApiProperty]] = None
    contains: typing.Optional[OpenApiProperty] = None
    min_contains: typing.Optional[int] = None
    max_contains: typing.Optional[int] = None
    default: typing.Optional[typing.List[typing.Any]] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["array"] = "array"

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


class OpenApiProperty_Object(pydantic_v1.BaseModel):
    properties: typing.Optional[typing.Dict[str, typing.Optional[OpenApiProperty]]] = None
    required: typing.Optional[typing.List[str]] = None
    min_properties: typing.Optional[int] = None
    max_properties: typing.Optional[int] = None
    property_names: typing.Optional[OpenApiProperty] = None
    additional_properties: typing.Optional[OpenApiProperty] = None
    pattern_properties: typing.Optional[typing.Dict[str, typing.Optional[OpenApiProperty]]] = None
    default: typing.Optional[typing.Dict[str, typing.Any]] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["object"] = "object"

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


class OpenApiProperty_Integer(pydantic_v1.BaseModel):
    minimum: typing.Optional[int] = None
    maximum: typing.Optional[int] = None
    exclusive_minimum: typing.Optional[bool] = None
    exclusive_maximum: typing.Optional[bool] = None
    default: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["integer"] = "integer"

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


class OpenApiProperty_Number(pydantic_v1.BaseModel):
    minimum: typing.Optional[float] = None
    maximum: typing.Optional[float] = None
    format: typing.Optional[str] = None
    exclusive_minimum: typing.Optional[bool] = None
    exclusive_maximum: typing.Optional[bool] = None
    default: typing.Optional[float] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["number"] = "number"

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


class OpenApiProperty_String(pydantic_v1.BaseModel):
    min_length: typing.Optional[int] = None
    max_length: typing.Optional[int] = None
    pattern: typing.Optional[str] = None
    format: typing.Optional[str] = None
    default: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["string"] = "string"

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


class OpenApiProperty_Boolean(pydantic_v1.BaseModel):
    default: typing.Optional[bool] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["boolean"] = "boolean"

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


class OpenApiProperty_OneOf(pydantic_v1.BaseModel):
    one_of: typing.List[OpenApiProperty] = pydantic_v1.Field(alias="oneOf")
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Literal["oneOf"] = "oneOf"

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
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


class OpenApiProperty_Const(pydantic_v1.BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    const: str
    type: typing.Literal["const"] = "const"

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


OpenApiProperty = typing.Union[
    OpenApiProperty_Array,
    OpenApiProperty_Object,
    OpenApiProperty_Integer,
    OpenApiProperty_Number,
    OpenApiProperty_String,
    OpenApiProperty_Boolean,
    OpenApiProperty_OneOf,
    OpenApiProperty_Const,
]
