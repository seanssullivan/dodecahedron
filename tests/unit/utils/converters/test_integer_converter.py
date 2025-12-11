# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import decimal

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_integer_from_boolean() -> None:
    result = converters.to_integer(True)
    assert result == 1


def test_returns_integer_from_decimal() -> None:
    result = converters.to_integer(decimal.Decimal("1.0"))
    assert result == 1


def test_returns_integer_from_float() -> None:
    result = converters.to_integer(1.0)
    assert result == 1


def test_returns_integer_from_integer() -> None:
    result = converters.to_integer(1)
    assert result == 1


@pytest.mark.parametrize("value", ["2.00 m", "2.0 m", "2.0", "2.", "2"])
def test_returns_integer_from_string(value: str) -> None:
    result = converters.to_integer(value)
    assert result == 2


def test_raises_error_when_string_cannot_be_converted() -> None:
    with pytest.raises(ValueError):
        converters.to_integer("failure")


def test_returns_default_when_none() -> None:
    result = converters.to_integer(None, 3)
    assert result == 3


def test_raises_error_when_default_is_not_type_integer() -> None:
    with pytest.raises(TypeError):
        converters.to_integer(None, "failure")  # type: ignore
