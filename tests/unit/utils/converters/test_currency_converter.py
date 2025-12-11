# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import decimal

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_amount_from_decimal() -> None:
    result = converters.to_currency(decimal.Decimal("1"))
    assert result == 1.00


def test_returns_amount_from_float() -> None:
    result = converters.to_currency(1.0)
    assert result == 1.00


def test_returns_amount_from_integer() -> None:
    result = converters.to_currency(1)
    assert result == 1.00


@pytest.mark.parametrize("value", ["2.000", "2.00", "2.0", "2.", "2"])
def test_returns_amount_from_string(value: str) -> None:
    result = converters.to_currency(value)
    assert result == 2.00


@pytest.mark.parametrize("value", ["4,000.00", "4,000.0", "4,000.", "4,000"])
def test_returns_amount_from_string_with_comma(value: str) -> None:
    result = converters.to_currency(value)
    assert result == 4000.00


def test_raises_error_when_string_cannot_be_converted() -> None:
    with pytest.raises(ValueError):
        converters.to_currency("failure")


def test_returns_default_when_none() -> None:
    result = converters.to_currency(None, 123.45)
    assert result == 123.45


def test_raises_error_when_default_is_not_type_float() -> None:
    with pytest.raises(TypeError):
        converters.to_currency(None, "failure")  # type: ignore
