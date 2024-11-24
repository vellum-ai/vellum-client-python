import pytest
from typing import ClassVar, Generic, List, TypeVar, Union

from vellum.workflows.outputs.base import BaseOutputs
from vellum.workflows.references.output import OutputReference
from vellum.workflows.types.utils import get_class_attr_names, infer_types


class ExampleClass:
    alpha: str
    beta = 3
    gamma: Union[str, int]
    epsilon = OutputReference(
        name="epsilon",
        types=(List[str],),
        instance=None,
        outputs_class=BaseOutputs,
    )
    zeta: ClassVar[str]
    eta: List[str]


T = TypeVar("T")


class ExampleGenericClass(Generic[T]):
    delta: T


class ExampleInheritedClass(ExampleClass):
    theta: int


@pytest.mark.parametrize(
    "cls, attr_name, expected_type",
    [
        (ExampleClass, "alpha", (str,)),
        (ExampleClass, "beta", (int,)),
        (ExampleClass, "gamma", (str, int)),
        (ExampleGenericClass, "delta", ()),
        (ExampleGenericClass[str], "delta", (str,)),
        (ExampleClass, "epsilon", (List[str],)),
        (ExampleClass, "zeta", (str,)),
        (ExampleClass, "eta", (List[str],)),
        (ExampleInheritedClass, "theta", (int,)),
        (ExampleInheritedClass, "alpha", (str,)),
        (ExampleInheritedClass, "beta", (int,)),
    ],
    ids=[
        "str",
        "int",
        "str_or_int",
        "generic_blank",
        "generic_str",
        "descriptor",
        "class_var",
        "list_str",
        "inherited_int",
        "inherited_parent_annotation",
        "inherited_parent_class_var",
    ],
)
def test_infer_types(cls, attr_name, expected_type):
    assert infer_types(cls, attr_name) == expected_type


@pytest.mark.parametrize(
    "cls, expected_attr_names",
    [
        (ExampleClass, {"alpha", "beta", "gamma", "epsilon", "zeta", "eta"}),
        (ExampleGenericClass, {"delta"}),
        (ExampleInheritedClass, {"alpha", "beta", "gamma", "epsilon", "zeta", "eta", "theta"}),
    ],
)
def test_class_attr_names(cls, expected_attr_names):
    assert get_class_attr_names(cls) == expected_attr_names
