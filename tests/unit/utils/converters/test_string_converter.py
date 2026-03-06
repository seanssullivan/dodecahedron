# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import decimal

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_string_from_boolean() -> None:
    result = converters.to_string(True)
    assert result == "True"


def test_returns_string_from_decimal() -> None:
    result = converters.to_string(decimal.Decimal("1.0"))
    assert result == "1.0"


def test_returns_string_from_float() -> None:
    result = converters.to_string(1.0)
    assert result == "1.0"


def test_returns_string_from_integer() -> None:
    result = converters.to_string(1)
    assert result == "1"


def test_returns_string_from_string() -> None:
    result = converters.to_string("success")
    assert result == "success"


def test_returns_default_when_none() -> None:
    result = converters.to_string(None, "success")
    assert result == "success"


def test_raises_error_when_default_is_not_type_string() -> None:
    with pytest.raises(TypeError):
        converters.to_string(None, 0)  # type: ignore
