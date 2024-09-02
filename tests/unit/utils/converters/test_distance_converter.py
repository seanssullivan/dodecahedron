# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


def test_returns_amount_from_integer() -> None:
    result = converters.to_distance(1)
    assert result == 1.0


@pytest.mark.parametrize("value", ["2.00 m", "2.0 m", "2.0", "2.", "2"])
def test_returns_amount_from_string(value) -> None:
    result = converters.to_distance(value)
    assert result == 2.0
