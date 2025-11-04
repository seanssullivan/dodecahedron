# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


@pytest.mark.parametrize("value", [True, 1, "true", "yes", "y", "1"])
def test_returns_y(value: Any) -> None:
    result = converters.to_y_or_n(value)
    assert result == "Y"


@pytest.mark.parametrize("value", [False, 0, "false", "no", "n", "0"])
def test_returns_n(value: Any) -> None:
    result = converters.to_y_or_n(value)
    assert result == "N"


def test_raises_error_for_invalid_default_value() -> None:
    with pytest.raises(ValueError):
        converters.to_y_or_n(None, "Failure")


def test_returns_default_when_none() -> None:
    result = converters.to_y_or_n(None, "N")
    assert result == "N"
