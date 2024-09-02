# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


@pytest.mark.parametrize("value", ["true", "yes", "y", "1"])
def test_returns_truthy_values(value) -> None:
    result = converters.to_boolean(value)
    assert result is True


@pytest.mark.parametrize("value", ["false", "no", "n", "0"])
def test_returns_falsey_values(value) -> None:
    result = converters.to_boolean(value)
    assert result is False


def test_returns_default_when_none() -> None:
    result = converters.to_boolean(None, True)
    assert result is True
