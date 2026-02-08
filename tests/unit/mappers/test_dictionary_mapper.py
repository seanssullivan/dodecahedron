# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import Dict
from typing import Hashable

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.mappers import DictMapper


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"name": "value"}),
        ({"value": "name"}, {}),
        ({"value": {"map_to": "name"}}, {}),
    ],
)
def test_instantiates_dictionary_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.from_dict({"name": "success"})
    assert isinstance(result, dict)
    assert result["value"] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({"value": {"map_to": "name", "converters": {"inward": int}}}, {})],
)
def test_converts_value_when_instantiating_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.from_dict({"name": "1"})
    assert isinstance(result["value"], int)


@pytest.mark.parametrize(
    "schema,properties",
    [({"value": {"map_to": "name", "default": "success"}}, {})],
)
def test_sets_default_value_when_instantiating_from_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.from_dict({})
    assert result["value"] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"value": 0}),
        ({0: "value"}, {}),
        ({0: {"map_to": "value"}}, {}),
    ],
)
def test_instantiates_class_from_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.from_list(["success"])
    assert isinstance(result, dict)
    assert result["value"] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({0: {"map_to": "value", "converters": {"inward": str}}}, {})],
)
def test_converts_value_when_instantiating_from_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.from_list([1])
    assert isinstance(result["value"], str)


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"name": "value"}),
        ({"value": "name"}, {}),
        ({"value": {"map_to": "name"}}, {}),
    ],
)
def test_converts_dictionary_to_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.to_dict({"value": "success"})
    assert isinstance(result, dict)
    assert result["name"] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({"value": {"map_to": "name", "converter": str}}, {})],
)
def test_converts_value_when_converting_to_dictionary(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.to_dict({"value": 1})
    assert isinstance(result["name"], str)


@pytest.mark.parametrize(
    "schema,properties",
    [
        ({}, {"value": 0}),
        ({0: "value"}, {}),
        ({0: {"map_to": "value"}}, {}),
    ],
)
def test_converts_class_to_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.to_list({"value": "success"})
    assert isinstance(result, list)
    assert result[0] == "success"


@pytest.mark.parametrize(
    "schema,properties",
    [({0: {"map_to": "value", "converter": int}}, {})],
)
def test_converts_value_when_converting_to_list(
    schema: Dict[Hashable, Any],
    properties: Dict[Hashable, Any],
) -> None:
    mapper = DictMapper(schema, properties)
    result = mapper.to_list({"value": "1"})
    assert isinstance(result[0], int)
