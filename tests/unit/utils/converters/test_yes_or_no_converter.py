# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


@pytest.mark.parametrize("value", [True, 1, "true", "yes", "y", "1"])
def test_returns_yes(value) -> None:
    result = converters.to_yes_or_no(value)
    assert result == "Yes"


@pytest.mark.parametrize("value", [False, 0, "false", "no", "n", "0"])
def test_returns_no(value) -> None:
    result = converters.to_yes_or_no(value)
    assert result == "No"


def test_raises_error_for_invalid_default_value() -> None:
    with pytest.raises(ValueError):
        converters.to_yes_or_no(None, "Failure")


def test_returns_default_when_none() -> None:
    result = converters.to_yes_or_no(None, "No")
    assert result == "No"
