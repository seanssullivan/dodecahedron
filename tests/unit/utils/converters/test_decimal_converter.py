# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import decimal

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_decimal_from_boolean() -> None:
    result = converters.to_decimal(True)
    assert result == decimal.Decimal("1")


def test_returns_decimal_from_decimal() -> None:
    result = converters.to_decimal(decimal.Decimal("1.0"))
    assert result == decimal.Decimal("1.0")


def test_returns_decimal_from_float() -> None:
    result = converters.to_decimal(1.0)
    assert result == decimal.Decimal("1.0")


def test_returns_decimal_from_integer() -> None:
    result = converters.to_decimal(1)
    assert result == decimal.Decimal("1.0")


@pytest.mark.parametrize("value", ["2.00 m", "2.0 m", "2.0", "2.", "2"])
def test_returns_decimal_from_string(value: str) -> None:
    result = converters.to_decimal(value)
    assert result == decimal.Decimal("2.0")


def test_raises_error_when_string_cannot_be_converted() -> None:
    with pytest.raises(ValueError):
        converters.to_decimal("failure")


def test_returns_default_when_none() -> None:
    result = converters.to_decimal(None, decimal.Decimal("3.0"))
    assert result == decimal.Decimal("3.0")


def test_raises_error_when_default_is_not_type_decimal() -> None:
    with pytest.raises(TypeError):
        converters.to_decimal(None, "failure")  # type: ignore
