import pytest

from vellum.workflows.utils.names import pascal_to_title_case


@pytest.mark.parametrize(
    ["input_str", "expected"],
    [
        ("MyPascalCaseString", "My Pascal Case String"),
        ("AnotherPascalCaseString", "Another Pascal Case String"),
    ],
)
def test_pascal_to_title_case(input_str, expected):
    actual = pascal_to_title_case(input_str)
    assert actual == expected
