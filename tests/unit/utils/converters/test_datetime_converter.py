# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime

# Third-Party Imports
from dateutil.tz import tzlocal
import pytest

# Local Imports
from dodecahedron.utils import converters


# Constants
NOW = datetime.datetime.now()
TODAY = datetime.date.today()


def test_returns_datetime_from_date() -> None:
    result = converters.to_datetime(TODAY)
    expected = make_datetime(TODAY).astimezone(tzlocal())
    assert result == expected


def test_returns_datetime_from_float() -> None:
    result = converters.to_datetime(NOW.timestamp())
    expected = NOW.astimezone(tzlocal())
    assert result == expected


def test_returns_datetime_from_integer() -> None:
    result = converters.to_datetime(int(NOW.timestamp()))
    expected = NOW.replace(microsecond=0).astimezone(tzlocal())
    assert result == expected


@pytest.mark.parametrize(
    "value",
    [
        NOW.strftime("%Y-%m-%d %H:%M:%S"),
        NOW.strftime("%Y/%m/%d %H:%M:%S"),
        NOW.strftime("%m/%d/%Y %H:%M:%S"),
    ],
)
def test_returns_datetime_from_string(value) -> None:
    result = converters.to_datetime(value)
    expected = NOW.replace(microsecond=0).astimezone(tzlocal())
    assert result == expected


def test_returns_default_when_none() -> None:
    result = converters.to_datetime(None, NOW)
    expected = NOW.astimezone(tzlocal())
    assert result == expected


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def make_datetime(__date: datetime.date) -> datetime.datetime:
    """Make datetime.

    Args:
        __date: Date.

    Returns:
        Datetime.

    """
    time = datetime.datetime.min.time()
    result = datetime.datetime.combine(__date, time)
    return result


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
