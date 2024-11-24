import datetime
import itertools
import json
import random
import re
from typing import Any, Callable, ClassVar, Dict, Generic, Mapping, Tuple, Type, TypeVar, Union, get_args

import dateutil.parser
import pydash
import pytz
import yaml

from vellum.workflows.errors import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.bases.base import BaseNodeMeta
from vellum.workflows.nodes.core.templating_node.custom_filters import is_valid_json_string
from vellum.workflows.nodes.core.templating_node.exceptions import JinjaTemplateError
from vellum.workflows.nodes.core.templating_node.render import render_sandboxed_jinja_template
from vellum.workflows.types.core import EntityInputsInterface
from vellum.workflows.types.generics import StateType
from vellum.workflows.types.utils import get_original_base

_DEFAULT_JINJA_GLOBALS: Dict[str, Any] = {
    "datetime": datetime,
    "dateutil": dateutil,
    "itertools": itertools,
    "json": json,
    "pydash": pydash,
    "pytz": pytz,
    "random": random,
    "re": re,
    "yaml": yaml,
}

_DEFAULT_JINJA_CUSTOM_FILTERS: Dict[str, Callable[[Union[str, bytes]], bool]] = {
    "is_valid_json_string": is_valid_json_string,
}

_OutputType = TypeVar("_OutputType")


# TODO: Consolidate all dynamic output metaclasses
# https://app.shortcut.com/vellum/story/5533
class _TemplatingNodeMeta(BaseNodeMeta):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]) -> Any:
        parent = super().__new__(mcs, name, bases, dct)

        if not isinstance(parent, _TemplatingNodeMeta):
            raise ValueError("TemplatingNode must be created with the TemplatingNodeMeta metaclass")

        parent.__dict__["Outputs"].__annotations__["result"] = parent.get_output_type()
        return parent

    def get_output_type(cls) -> Type:
        original_base = get_original_base(cls)
        all_args = get_args(original_base)

        if len(all_args) < 2 or isinstance(all_args[1], TypeVar):
            return str
        else:
            return all_args[1]


class TemplatingNode(BaseNode[StateType], Generic[StateType, _OutputType], metaclass=_TemplatingNodeMeta):
    """Used to render a Jinja template.

    Useful for lightweight data transformations and complex string templating.
    """

    # The Jinja template to render.
    template: ClassVar[str]

    # The inputs to render the template with.
    inputs: ClassVar[EntityInputsInterface]

    jinja_globals: Dict[str, Any] = _DEFAULT_JINJA_GLOBALS
    jinja_custom_filters: Mapping[str, Callable[[Union[str, bytes]], bool]] = _DEFAULT_JINJA_CUSTOM_FILTERS

    class Outputs(BaseNode.Outputs):
        # We use our mypy plugin to override the _OutputType with the actual output type
        # for downstream references to this output.
        result: _OutputType  # type: ignore[valid-type]

    def _cast_rendered_template(self, rendered_template: str) -> Any:
        original_base = get_original_base(self.__class__)
        all_args = get_args(original_base)

        if len(all_args) < 2 or isinstance(all_args[1], TypeVar):
            output_type = str
        else:
            output_type = all_args[1]

        if output_type is str:
            return rendered_template

        if output_type is float:
            return float(rendered_template)

        if output_type is int:
            return int(rendered_template)

        if output_type is bool:
            return bool(rendered_template)

        raise ValueError(f"Unsupported output type: {output_type}")

    def run(self) -> Outputs:
        rendered_template = self._render_template()
        result = self._cast_rendered_template(rendered_template)

        return self.Outputs(result=result)

    def _render_template(self) -> str:
        try:
            return render_sandboxed_jinja_template(
                template=self.template,
                input_values=self.inputs,
                jinja_custom_filters={**self.jinja_custom_filters},
                jinja_globals=self.jinja_globals,
            )
        except JinjaTemplateError as e:
            raise NodeException(message=str(e), code=VellumErrorCode.INVALID_TEMPLATE)
