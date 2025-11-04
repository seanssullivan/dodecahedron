# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


@pytest.mark.parametrize("value", [datetime.date.today()])
def test_returns_true_from_date(value: datetime.date) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", [datetime.datetime.now()])
def test_returns_true_from_datetime(value: datetime.datetime) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value,expected", [(0.0, False), (1.0, True)])
def test_returns_boolean_from_float(value: float, expected: bool) -> None:
    result = converters.to_boolean(value)
    assert result == expected


@pytest.mark.parametrize("value,expected", [(0, False), (1, True)])
def test_returns_boolean_from_integer(value: int, expected: bool) -> None:
    result = converters.to_boolean(value)
    assert result == expected


@pytest.mark.parametrize("value", ["true", "yes", "y", "1"])
def test_returns_true_from_string_for_truthy_values(value: str) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", ["false", "no", "n", "0"])
def test_returns_false_from_string_for_falsey_values(value: str) -> None:
    result = converters.to_boolean(value)
    assert result is False


def test_returns_default_when_none() -> None:
    result = converters.to_boolean(None, True)
    assert result is True
