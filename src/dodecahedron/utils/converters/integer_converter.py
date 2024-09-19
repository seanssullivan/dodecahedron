# -*- coding: utf-8 -*-
"""Integer Converter.

Module provides function for converting values to integers.

"""

# Standard Library Imports
import datetime
import decimal
import time
import typing

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_integer"]


def to_integer(__value: typing.Any, /, default: int = 0) -> int:
    """Convert value to integer.

    Args:
        __value: Value to convert to integer.
        default (optional): Default value. Default ``0``.

    Returns:
        Integer.

    """
    converter = IntegerConverter(default=default)
    result = converter(__value)
    return result


class IntegerConverter(BaseConverter):
    """Class implements a integer converter.

    Args:
        default (optional): Default value. Default ``0``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: int = 0,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, int):
            message = f"expected type 'int', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def int_from_bool(__value: bool, _: int, /) -> int:
    """Convert boolean value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = int(__value)
    return result


def int_from_date(__value: datetime.date, _: int, /) -> int:
    """Convert date value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    timestamp = time.mktime(__value.timetuple())
    result = int(timestamp)
    return result


def int_from_datetime(__value: datetime.datetime, _: int, /) -> int:
    """Convert datetime value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    timestamp = __value.timestamp()
    result = int(timestamp)
    return result


def int_from_decimal(__value: decimal.Decimal, _: int, /) -> int:
    """Convert decimal value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = int(__value)
    return result


def int_from_float(__value: float, _: int, /) -> int:
    """Convert float value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = int(__value)
    return result


def int_from_int(__value: int, _: int, /) -> int:
    """Convert integer value to ``int``.

    Args:
        __value: Value to convert to ``int``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = int(__value)
    return result


def int_from_str(__value: str, default: int = 0, /) -> int:
    """Convert string value to ``int``.

    Args:
        __value: Value to convert to ``int``.
        default (optional): Default value. Default ``0``.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to ``int``.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        result = int(float(value))
    except ValueError:
        message = f"{__value} cannot be converted to int"
        raise ValueError(message)
    else:
        return result


DEFAULT_CONVERSIONS = {
    bool: int_from_bool,
    datetime.date: int_from_date,
    datetime.datetime: int_from_datetime,
    decimal.Decimal: int_from_decimal,
    float: int_from_float,
    int: int_from_int,
    str: int_from_str,
}  # type: typing.Dict[type, typing.Callable]
