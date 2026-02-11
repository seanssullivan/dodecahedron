# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime
import decimal
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


@pytest.mark.parametrize("value", [True, False])
def test_returns_boolean_from_boolean(value: bool) -> None:
    result = converters.to_boolean(value)
    assert result is value


@pytest.mark.parametrize("value", [datetime.date.today()])
def test_returns_true_from_date(value: datetime.date) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [datetime.datetime.now()])
def test_returns_true_from_datetime(value: datetime.datetime) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [decimal.Decimal("1")])
def test_returns_true_from_decimal(value: decimal.Decimal) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [{"key": True}, {"key": 1}, {"key": "yes"}])
def test_returns_true_from_dictionary(value: Dict[Hashable, Any]) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [{"key": False}, {"key": 0}, {"key": "no"}])
def test_returns_false_from_dictionary(value: Dict[Hashable, Any]) -> None:
    result = converters.to_boolean(value)
    assert result is False


@pytest.mark.parametrize("value,expected", [(0.0, False), (1.0, True)])
def test_returns_boolean_from_float(value: float, expected: bool) -> None:
    result = converters.to_boolean(value)
    assert result == expected


@pytest.mark.parametrize("value,expected", [(0, False), (1, True)])
def test_returns_boolean_from_integer(value: int, expected: bool) -> None:
    result = converters.to_boolean(value)
    assert result == expected


@pytest.mark.parametrize("value", [[True], [1], ["yes"]])
def test_returns_true_from_list_with_truthy_values(value: List[Any]) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [[False], [0], ["no"]])
def test_returns_false_from_list_with_falsy_values(value: List[Any]) -> None:
    result = converters.to_boolean(value)
    assert result is False


@pytest.mark.parametrize("value", [[False, True, 0, "yes"]])
def test_returns_false_from_list_with_mixed_values(value: List[Any]) -> None:
    result = converters.to_boolean(value)
    assert result is False


@pytest.mark.parametrize("value", ["true", "yes", "y", "1"])
def test_returns_true_from_string_for_truthy_values(value: str) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", ["false", "no", "n", "0"])
def test_returns_false_from_string_for_falsey_values(value: str) -> None:
    result = converters.to_boolean(value)
    assert result is False


def test_returns_default_when_empty_string() -> None:
    result = converters.to_boolean("", False)
    assert result is False


def test_returns_default_when_none() -> None:
    result = converters.to_boolean(None, True)
    assert result is True


def test_raises_error_when_default_is_not_type_bool() -> None:
    with pytest.raises(TypeError):
        converters.to_boolean(None, "failure")  # type: ignore
