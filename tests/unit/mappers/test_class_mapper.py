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
    [({"value": {"map_to": "_value", "converters": {"inward": str}}}, {})],
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
    [({"value": {"map_to": "_value", "default": "success"}}, {})],
)
def test_sets_default_value_when_instantiating_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.from_dict({})
    assert result.value == "success"


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


@pytest.mark.parametrize(
    "schema,properties",
    [({0: {"map_to": "_value", "converters": {"inward": str}}}, {})],
)
def test_converts_value_when_instantiating_from_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.from_list([1])
    assert isinstance(result.value, str)


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"_value": "value"}),
        ({"value": "_value"}, {}),
        ({"value": {"map_to": "_value"}}, {}),
    ],
)
def test_converts_class_to_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.to_dict(ExampleClass("success"))
    assert isinstance(result, dict)
    assert result["value"] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({"value": {"map_to": "_value", "converter": int}}, {})],
)
def test_converts_value_when_converting_to_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.to_dict(ExampleClass("1"))
    assert isinstance(result["value"], int)


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"_value": 0}),
        ({0: "_value"}, {}),
        ({0: {"map_to": "_value"}}, {}),
    ],
)
def test_converts_class_to_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.to_list(ExampleClass("success"))
    assert isinstance(result, list)
    assert result[0] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({0: {"map_to": "_value", "converter": int}}, {})],
)
def test_converts_value_when_converting_to_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = ClassMapper(ExampleClass, schema, properties)
    result = mapper.to_list(ExampleClass("1"))
    assert isinstance(result[0], int)
