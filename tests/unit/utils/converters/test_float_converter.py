# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import decimal

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_float_from_boolean() -> None:
    result = converters.to_float(True)
    assert result == 1.0


def test_returns_float_from_decimal() -> None:
    result = converters.to_float(decimal.Decimal("1.0"))
    assert result == 1.0


def test_returns_float_from_float() -> None:
    result = converters.to_float(1.0)
    assert result == 1.0


def test_returns_float_from_integer() -> None:
    result = converters.to_float(1)
    assert result == 1.0


@pytest.mark.parametrize("value", ["2.50 m", "2.5 m", "2.5"])
def test_returns_float_from_string(value: str) -> None:
    result = converters.to_float(value)
    assert result == 2.5


def test_raises_error_when_string_cannot_be_converted() -> None:
    with pytest.raises(ValueError):
        converters.to_float("failure")


def test_returns_default_when_none() -> None:
    result = converters.to_float(None, 3.0)
    assert result == 3.0


def test_raises_error_when_default_is_not_type_float() -> None:
    with pytest.raises(TypeError):
        converters.to_float(None, "failure")  # type: ignore
