# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_amount_from_integer() -> None:
    result = converters.to_currency(1)
    assert result == 1.00


@pytest.mark.parametrize("value", ["2.000", "2.00", "2.0", "2.", "2"])
def test_returns_amount_from_string(value) -> None:
    result = converters.to_currency(value)
    assert result == 2.00


@pytest.mark.parametrize("value", ["4,000.00", "4,000.0", "4,000.", "4,000"])
def test_returns_amount_from_string_with_comma(value) -> None:
    result = converters.to_currency(value)
    assert result == 4000.00


def test_returns_default_when_none() -> None:
    result = converters.to_currency(None, 123.45)
    assert result == 123.45
