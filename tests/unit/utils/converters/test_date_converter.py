# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import converters


# Constants
NOW = datetime.datetime.now()
TODAY = datetime.date.today()


def test_returns_date_from_datetime() -> None:
    result = converters.to_date(NOW)
    assert result == TODAY


def test_returns_date_from_float() -> None:
    result = converters.to_date(NOW.timestamp())
    assert result == TODAY


def test_returns_date_from_integer() -> None:
    timestamp = make_timestamp(TODAY)
    result = converters.to_date(int(timestamp))
    assert result == TODAY


@pytest.mark.parametrize(
    "value",
    [
        TODAY.strftime("%Y-%m-%d"),
        TODAY.strftime("%Y/%m/%d"),
        TODAY.strftime("%m/%d/%Y"),
    ],
)
def test_returns_date_from_string(value: str) -> None:
    result = converters.to_date(value)
    assert result == TODAY


def test_returns_default_when_none() -> None:
    result = converters.to_date(None, TODAY)
    assert result == TODAY


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def make_timestamp(__date: datetime.date) -> float:
    """Make timestamp.

    Args:
        __date: Date.

    Returns:
        Timestamp.

    """
    time = datetime.datetime.min.time()
    result = datetime.datetime.combine(__date, time).timestamp()
    return result
