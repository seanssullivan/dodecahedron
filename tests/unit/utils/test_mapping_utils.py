# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import mapping_utils as utils


def test_deep_get_returns_value_from_dictionary() -> None:
    m: Dict[Hashable, Any] = {"first": "success"}
    result = utils.deep_get(m, "first")
    assert result == "success"


def test_deep_get_returns_value_from_list() -> None:
    m: List[Any] = ["failure", "success"]
    result = utils.deep_get(m, "1")
    assert result == "success"


def test_deep_get_returns_value_from_nested_dictionaries() -> None:
    d: Dict[Hashable, Any] = {"first": {"second": "success"}}
    result = utils.deep_get(d, "first.second")
    assert result == "success"


def test_deep_get_returns_value_from_nested_lists() -> None:
    m: List[Any] = [["failure"], ["success"]]
    result = utils.deep_get(m, "1.0")
    assert result == "success"


def test_deep_get_returns_value_from_nested_objects() -> None:
    d: Dict[Hashable, Any] = {"first": {"second": ["failure", "success"]}}
    result = utils.deep_get(d, "first.second.1")
    assert result == "success"


@pytest.mark.parametrize("key", ["1.2", "'1'.'2'", '"1"."2"', "[1].[2]"])
def test_deep_get_supports_numerical_keys(key: str) -> None:
    d: Dict[Hashable, Any] = {"1": {"2": "success"}}
    result = utils.deep_get(d, key)
    assert result == "success"


def test_deep_set_returns_dictionary() -> None:
    result = utils.deep_set({}, "key", "test")
    assert isinstance(result, dict)


def test_deep_set_updates_nested_dictionary() -> None:
    d: Dict[Hashable, Any] = {"parent": {"child": {"name": "failure"}}}
    result = utils.deep_set(d, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


def test_deep_set_creates_nested_dictionaries() -> None:
    result = utils.deep_set({}, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


def test_deep_set_replaces_none_with_dictionary() -> None:
    d: Dict[Hashable, Any] = {"parent": {"child": None}}
    result = utils.deep_set(d, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


@pytest.mark.parametrize("value", ["test", 1.0, [1, 2, 3]])
def test_raises_key_error(value: Any) -> None:
    d: Dict[Hashable, Any] = {"parent": {"child": value}}
    with pytest.raises(KeyError, match="parent.child"):
        utils.deep_set(d, "parent.child.name", "success")
