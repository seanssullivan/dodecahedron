# -*- coding: utf-8 -*-
"""Decimal Converter.

Module provides function for converting values to decimals.

"""

# Standard Library Imports
import datetime
import decimal
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal
from typing import Optional

# Local Imports
from .base_converter import BaseConverter
from .. import parsers

__all__ = ["to_decimal"]


def to_decimal(
    __value: Any, /, default: decimal.Decimal = decimal.Decimal("0.0")
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
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, decimal.Decimal):  # type: ignore
            message = f"expected type 'Decimal', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()

    @property
    def default(self) -> Any:  # pragma: no cover
        """Default value."""
        return self._default

    @default.setter
    def default(self, value: Any) -> None:  # pragma: no cover
        if not isinstance(value, decimal.Decimal):  # type: ignore
            message = f"expected type 'Decimal', got {type(value)} instead"
            raise TypeError(message)

        self._default = value


def decimal_from_bool(__value: bool, _: decimal.Decimal, /) -> decimal.Decimal:
    """Convert boolean value to decimal.

    Args:
        __value: Value to convert to decimal.

    Returns:
        Decimal.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):  # type: ignore  # pragma: no cover
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
    if not isinstance(__value, datetime.date):  # type: ignore  # pragma: no cover
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
    if not isinstance(__value, datetime.datetime):  # type: ignore  # pragma: no cover
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
    if not isinstance(__value, decimal.Decimal):  # type: ignore  # pragma: no cover
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
    if not isinstance(__value, float):  # type: ignore  # pragma: no cover
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
    if not isinstance(__value, int):  # type: ignore  # pragma: no cover
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = decimal.Decimal(__value)
    return result


def decimal_from_str(
    __value: str,
    default: Optional[decimal.Decimal] = decimal.Decimal("0.0"),
    /,
) -> Optional[decimal.Decimal]:
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
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        number = parsers.parse_number(value)
        result = decimal.Decimal(str(number))

    except (decimal.InvalidOperation, ValueError):
        message = f"'{__value}' cannot be converted to decimal"
        raise ValueError(message)

    return result


DEFAULT_CONVERSIONS: Dict[type, Callable[..., Optional[decimal.Decimal]]] = {
    bool: decimal_from_bool,
    datetime.date: decimal_from_date,
    datetime.datetime: decimal_from_datetime,
    decimal.Decimal: decimal_from_decimal,
    float: decimal_from_float,
    int: decimal_from_int,
    str: decimal_from_str,
}
