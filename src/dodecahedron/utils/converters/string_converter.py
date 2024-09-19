# -*- coding: utf-8 -*-
"""String Converter.

Module provides function for converting values to strings.

"""

# Standard Library Imports
import datetime
import decimal
import typing

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_string"]


def to_string(
    __value: object, /, default: typing.Optional[str] = None
) -> typing.Optional[str]:
    """Convert value to string.

    Args:
        value: Value to convert.

    Returns:
        String.

    """
    converter = StringConverter(default=default)
    result = converter(__value)
    return result


class StringConverter(BaseConverter):
    """Class implements a string converter.

    Args:
        default (optional): Default value. Default ``None``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: typing.Optional[str] = None,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if default and not isinstance(default, str):
            message = f"expected type 'str', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def str_from_bool(__value: bool, _: typing.Optional[str] = None, /) -> str:
    """Convert boolean value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_date(
    __value: datetime.date, _: typing.Optional[str] = None, /
) -> str:
    """Convert date value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_datetime(
    __value: datetime.datetime, _: typing.Optional[str] = None, /
) -> str:
    """Convert datetime value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_decimal(
    __value: decimal.Decimal, _: typing.Optional[str] = None, /
) -> int:
    """Convert decimal value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_float(__value: float, _: typing.Optional[str] = None, /) -> str:
    """Convert float value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_int(__value: int, _: typing.Optional[str] = None, /) -> str:
    """Convert integer value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_str(
    __value: str, default: typing.Optional[str] = None, /
) -> typing.Optional[str]:
    """Convert string value to ``str``.

    Args:
        __value: Value to convert to ``str``.
        default (optional): Default value. Default ``None``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to ``str``.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    result = str(__value)
    return result


DEFAULT_CONVERSIONS = {
    bool: str_from_bool,
    datetime.date: str_from_date,
    datetime.datetime: str_from_datetime,
    decimal.Decimal: str_from_decimal,
    float: str_from_float,
    int: str_from_int,
    str: str_from_str,
}  # type: typing.Dict[type, typing.Callable]
