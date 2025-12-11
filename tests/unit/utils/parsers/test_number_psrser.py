# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import parsers


@pytest.mark.parametrize("value,expected", [("2.50 m", 2.5)])
def test_parses_number_from_string(value: str, expected: float) -> None:
    result = parsers.parse_number(value)
    assert result == expected


@pytest.mark.parametrize("value,expected", [("2.", 2.0)])
def test_removes_trailing_period(value: str, expected: float) -> None:
    result = parsers.parse_number(value)
    assert result == expected
