# -*- coding: utf-8 -*-
"""Datetime Converter.

Module provides function for converting values to datatimes.

"""

# Standard Library Imports
import datetime
import decimal
import typing

# Third-Party Imports
import cachetools
from cachetools.keys import hashkey
from dateutil.parser import parse
from dateutil.parser import ParserError
from dateutil.tz import tzlocal
import pytz

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_datetime"]


def to_datetime(
    __value: typing.Any,
    /,
    default: typing.Optional[datetime.datetime] = None,
    timezone: typing.Optional[typing.Union[str, datetime.tzinfo]] = tzlocal(),
) -> typing.Optional[datetime.datetime]:
    """Convert value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.
        default (optional): Default value. Default ``None``.
        timezone (optional): Timezone. Default `local`.

    Returns:
        Datetime.

    """
    converter = DatetimeConverter(default=default, timezone=timezone)
    result = converter(__value)
    return result


class DatetimeConverter(BaseConverter):
    """Class implements a datetime converter.

    Args:
        default (optional): Default value. Default ``None``.
        timezone (optional): Timezone. Default ``None``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: typing.Optional[datetime.datetime] = None,
        timezone: typing.Optional[typing.Union[str, datetime.tzinfo]] = None,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if default and not isinstance(default, datetime.datetime):
            message = f"expected type 'datetime', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()
        self._timezone = timezone

    def __call__(
        self, __value: typing.Any, /
    ) -> typing.Optional[datetime.datetime]:
        dt = super().__call__(__value)
        result = self._add_timezone(dt)
        return result

    def _add_timezone(
        self, __datetime: typing.Optional[datetime.datetime]
    ) -> typing.Optional[datetime.datetime]:
        """Add timezone.

        Args:
            __datetime: Datetime.

        Returns:
            Datetime.

        """
        if not __datetime or self._timezone is None:
            return __datetime

        if isinstance(self._timezone, str) and is_naive(__datetime):
            result = pytz.timezone(self._timezone).localize(__datetime)
            return result

        result = __datetime.astimezone(self._timezone)
        return result


def datetime_from_date(
    __value: datetime.date, _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert date value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    time = datetime.datetime.min.time()
    result = datetime.datetime.combine(__value, time)
    return result


def datetime_from_datetime(
    __value: datetime.datetime, _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert datetime value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime.datetime(
        __value.year,
        __value.month,
        __value.day,
        __value.hour,
        __value.minute,
        __value.second,
        __value.microsecond,
        __value.tzinfo,
    )
    return result


def datetime_from_decimal(
    __value: decimal.Decimal, _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert decimal value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime_from_float(float(__value), _)
    return result


def datetime_from_float(
    __value: float, _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert float value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    try:
        result = datetime_from_serial_date(__value, _)
    except ValueError:
        result = datetime_from_timestamp(__value, _)

    return result


def datetime_from_serial_date(
    __value: float, _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert serial date value to ``datetime``.

    Implementation based on reply to a question on Stack Overflow.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'float'.

    .. _Stack Overflow:
        https://stackoverflow.com/a/6706556/16732779

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    seconds = (__value - 25569) * 86400.0
    result = datetime_from_timestamp(seconds, _)
    return result


def datetime_from_int(
    __value: int, _: typing.Optional[datetime.datetime], /
) -> datetime.date:
    """Convert integer value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime_from_timestamp(float(__value), _)
    return result


def datetime_from_timestamp(
    __value: typing.Union[float, int], _: typing.Optional[datetime.datetime], /
) -> datetime.datetime:
    """Convert timestamp value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime.datetime.fromtimestamp(__value)
    return result


@cachetools.cached(cachetools.LRUCache(maxsize=1000), hashkey)
def datetime_from_str(
    __value: str, default: typing.Optional[datetime.datetime] = None, /
) -> typing.Optional[datetime.datetime]:
    """Convert string value to ``datetime``.

    Args:
        __value: String representation of datetime.
        default (optional): Default value. Default ``None``.

    Returns:
        Datetime.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to ``datetime``.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        result = parse(value) if value else default

    except (ParserError, ValueError) as error:
        message = f"'{__value}' cannot be converted to datetime"
        raise ValueError(message) from error

    return result


DEFAULT_CONVERSIONS = {
    datetime.date: datetime_from_date,
    datetime.datetime: datetime_from_datetime,
    decimal.Decimal: datetime_from_decimal,
    float: datetime_from_float,
    int: datetime_from_int,
    str: datetime_from_str,
}  # type: typing.Dict[type, typing.Callable]


# ----------------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------------
def is_naive(__dt: datetime.datetime) -> bool:
    """Check whether datetime is naive.

    Args:
        __dt: Datetime.

    Returns:
        Wether datetime is naive.

    """
    result = __dt.tzinfo is None or __dt.tzinfo.utcoffset(__dt) is None
    return result
