# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime
import decimal

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


def test_returns_datetime_from_datetime() -> None:
    result = converters.to_datetime(NOW)
    expected = NOW.astimezone(tzlocal())
    assert result == expected


def test_returns_datetime_from_decimal() -> None:
    value = decimal.Decimal(str(NOW.timestamp()))
    result = converters.to_datetime(value)
    expected = NOW.astimezone(tzlocal())
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
def test_returns_datetime_from_string(value: str) -> None:
    result = converters.to_datetime(value)
    expected = NOW.replace(microsecond=0).astimezone(tzlocal())
    assert result == expected


def test_raises_error_when_string_cannot_be_converted() -> None:
    with pytest.raises(ValueError):
        converters.to_datetime("failure")


def test_returns_default_when_none() -> None:
    result = converters.to_datetime(None, NOW)
    expected = NOW.astimezone(tzlocal())
    assert result == expected


def test_raises_error_when_default_is_not_type_datetime() -> None:
    with pytest.raises(TypeError):
        converters.to_datetime(None, "failure")  # type: ignore


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
