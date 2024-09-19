# -*- coding: utf-8 -*-
"""Timestamp Converter.

Module provides function for converting values to timestamps.

"""

# Standard Library Imports
import datetime
import decimal
import time
import typing

# Third-Party Imports
from dateutil.parser import parse
from dateutil.parser import ParserError

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_timestamp"]


def to_timestamp(__value: typing.Any, /, default: float = 0.0) -> float:
    """Convert date to timestamp.

    Args:
        __value: Value to convert to timestamp.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Timestamp.
    """
    converter = TimestampConverter(default=default)
    result = converter(__value)
    return result


class TimestampConverter(BaseConverter):
    """Class implements a timestamp converter.

    Args:
        default (optional): Default value. Default ``0.0``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: float = 0.0,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def timestamp_from_date(
    __value: datetime.date, _: typing.Optional[float] = None, /
) -> float:
    """Convert date value to timestamp.

    Args:
        __value: Value to convert to timestamp.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = time.mktime(__value.timetuple())
    return result


def timestamp_from_datetime(
    __value: datetime.datetime, _: typing.Optional[float] = None, /
) -> float:
    """Convert datetime value to timestamp.

    Args:
        __value: Value to convert to timestamp.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = __value.timestamp()
    return result


def timestamp_from_decimal(
    __value: decimal.Decimal, _: typing.Optional[float] = None, /
) -> int:
    """Convert decimal value to timestamp.

    Args:
        __value: Value to convert to timestamp.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def timestamp_from_float(
    __value: float, _: typing.Optional[float] = None, /
) -> float:
    """Convert float value to timestamp.

    Args:
        __value: Value to convert to timestamp.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def timestamp_from_int(
    __value: int, _: typing.Optional[float] = None, /
) -> float:
    """Convert integer value to timestamp.

    Args:
        __value: Value to convert to timestamp.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def timestamp_from_str(
    __value: str, default: typing.Optional[float] = None, /
) -> typing.Optional[float]:
    """Convert string value to timestamp.

    Args:
        __value: Value to convert to timestamp.
        default (optional): Default value. Default ``None``.

    Returns:
        Timestamp.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to timestamp.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        result = parse(value).timestamp() if value else default

    except (ParserError, ValueError) as error:
        message = f"'{__value}' cannot be converted to timestamp"
        raise ValueError(message) from error

    return result


DEFAULT_CONVERSIONS = {
    datetime.date: timestamp_from_date,
    datetime.datetime: timestamp_from_datetime,
    decimal.Decimal: timestamp_from_decimal,
    float: timestamp_from_float,
    int: timestamp_from_int,
    str: timestamp_from_str,
}  # type: typing.Dict[type, typing.Callable]
