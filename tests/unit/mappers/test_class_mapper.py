# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import Dict
from typing import Hashable

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.mappers import ClassMapper


class ExampleClass:
    """An example implementation of a model class.

    Args:
        value: Value.

    Raises:
        ValueError: when argument is ``None``.

    """

    def __init__(self, value: Any = None) -> None:
        if value is None:
            raise ValueError("argument cannot be 'None'")

        self._value = value

    @property
    def value(self) -> Any:
        """Value"""
        return self._value


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"_value": "value"}),
        ({"value": "_value"}, {}),
        ({"value": {"map_to": "_value"}}, {}),
    ],
)
def test_instantiates_class_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.from_dict({"value": "success"})
    assert isinstance(result, ExampleClass)
    assert result.value == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({"value": {"map_to": "_value", "converter": str}}, {})],
)
def test_converts_value_when_instantiating_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.from_dict({"value": 1})
    assert isinstance(result.value, str)


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"_value": 0}),
        ({0: "_value"}, {}),
        ({0: {"map_to": "_value"}}, {}),
    ],
)
def test_instantiates_class_from_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.from_list(["success"])
    assert isinstance(result, ExampleClass)
    assert result.value == "success"
