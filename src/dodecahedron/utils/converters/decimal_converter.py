# -*- coding: utf-8 -*-
"""Decimal Converter.

Module provides function for converting values to decimals.

"""

# Standard Library Imports
import datetime
import decimal
import re
import time
import typing

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_decimal"]


def to_decimal(
    __value: typing.Any, /, default: decimal.Decimal = decimal.Decimal("0.0")
) -> decimal.Decimal:
    """Convert value to decimal.

    Args:
        __value: Value to convert to decimal.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Decimal.

    """
    converter = DecimalConverter(default=default)
    result = converter(__value)
    return result


class DecimalConverter(BaseConverter):
    """Class implements a decimal converter.

    Args:
        default (optional): Default value. Default ``0.0``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: decimal.Decimal = decimal.Decimal("0.0"),
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def decimal_from_bool(__value: bool, _: decimal.Decimal, /) -> decimal.Decimal:
    """Convert boolean value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = decimal.Decimal(__value)
    return result


def decimal_from_date(
    __value: datetime.date, _: decimal.Decimal, /
) -> decimal.Decimal:
    """Convert date value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    value = time.mktime(__value.timetuple())
    result = decimal.Decimal(str(value))
    return result


def decimal_from_datetime(
    __value: datetime.datetime, _: decimal.Decimal, /
) -> decimal.Decimal:
    """Convert datetime value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.timestamp()
    result = decimal.Decimal(str(value))
    return result


def decimal_from_decimal(
    __value: decimal.Decimal, _: decimal.Decimal, /
) -> decimal.Decimal:
    """Convert decimal value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = decimal.Decimal(__value)
    return result


def decimal_from_float(
    __value: float, _: decimal.Decimal, /
) -> decimal.Decimal:
    """Convert float value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = decimal.Decimal(str(__value))
    return result


def decimal_from_int(__value: int, _: decimal.Decimal, /) -> decimal.Decimal:
    """Convert integer value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = decimal.Decimal(__value)
    return result


def decimal_from_str(
    __value: str,
    default: typing.Optional[decimal.Decimal] = decimal.Decimal("0.0"),
    /,
) -> decimal.Decimal:
    """Convert string value to decimal.

    Args:
        __value: String representation of decimal value.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to decimal.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        result = decimal.Decimal(re.sub(r"[^0-9a-zA-Z.]+", r"", value))
    except decimal.InvalidOperation:
        message = f"'{__value}' cannot be converted to decimal"
        raise ValueError(message)
    else:
        return result


DEFAULT_CONVERSIONS = {
    bool: decimal_from_bool,
    datetime.date: decimal_from_date,
    datetime.datetime: decimal_from_datetime,
    decimal.Decimal: decimal_from_decimal,
    float: decimal_from_float,
    int: decimal_from_int,
    str: decimal_from_str,
}  # type: typing.Dict[type, typing.Callable]
