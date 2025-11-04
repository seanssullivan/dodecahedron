# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_float_from_integer() -> None:
    result = converters.to_float(1)
    assert result == 1.0


@pytest.mark.parametrize("value", ["2.00 m", "2.0 m", "2.0", "2.", "2"])
def test_returns_float_from_string(value: str) -> None:
    result = converters.to_float(value)
    assert result == 2.0


def test_returns_default_when_none() -> None:
    result = converters.to_float(None, 3.0)
    assert result == 3.0
