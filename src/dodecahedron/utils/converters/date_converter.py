# -*- coding: utf-8 -*-
"""Date Converter.

Module provides function for converting values to dates.

"""

# Standard Library Imports
import datetime
import decimal
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union

# Third-Party Imports
import cachetools
from cachetools.keys import hashkey
from dateutil.parser import parse
from dateutil.parser import ParserError

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_date"]


def to_date(
    __value: Any, /, default: Optional[datetime.date] = None
) -> Optional[datetime.date]:
    """Converts value to date.

    Args:
        __value: Date.
        default (optional): Default value. Default ``None``.

    Returns:
        Date.

    """
    converter = DateConverter(default=default)
    result = converter(__value)
    return result


class DateConverter(BaseConverter):
    """Class implements a date converter.

    Args:
        default (optional): Default value. Default ``None``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: Optional[datetime.date] = None,
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        if default and not isinstance(default, datetime.date):  # type: ignore
            message = f"expected type 'date', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def date_from_date(
    __value: datetime.date, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert date value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):  # type: ignore
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime.date(__value.year, __value.month, __value.day)
    return result


def date_from_datetime(
    __value: datetime.datetime, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert datetime value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):  # type: ignore
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = __value.date()
    return result


def date_from_decimal(
    __value: decimal.Decimal, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert decimal value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):  # type: ignore
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = date_from_float(float(__value), _)
    return result


def date_from_float(
    __value: float, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert float value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    try:
        result = date_from_serial_date(__value, _)

    except ValueError:
        result = date_from_timestamp(__value, _)

    return result


def date_from_serial_date(
    __value: float, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert serial date value to ``date``.

    Implementation based on answer from Stack Overflow.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'float'.

    .. _Stack Overflow:
        https://stackoverflow.com/a/6706556/16732779

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    seconds = (__value - 25569) * 86400.0
    result = date_from_timestamp(seconds, _)
    return result


def date_from_int(
    __value: int, _: Optional[datetime.date], /
) -> datetime.date:
    """Convert integer value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):  # type: ignore
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = date_from_timestamp(__value, _)
    return result


@cachetools.cached(cachetools.LRUCache(maxsize=1000), hashkey)
def date_from_str(
    __value: str, default: Optional[datetime.date] = None, /
) -> Optional[datetime.date]:
    """Convert string value to ``date``.

    Args:
        __value: String representation of date.
        default (optional): Default value. Default ``None``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to ``date``.

    """
    if not isinstance(__value, str):  # type: ignore
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        result = parse(value).date() if value else default

    except (ParserError, ValueError) as error:
        message = f"'{__value}' cannot be converted to date"
        raise ValueError(message) from error

    return result


def date_from_timestamp(
    __value: Union[float, int], _: Optional[datetime.date], /
) -> datetime.date:
    """Convert timestamp value to ``date``.

    Args:
        __value: Value to convert to ``date``.

    Returns:
        Date.

    Raises:
        TypeError: when value is not type 'float' or 'int'.

    """
    if not isinstance(__value, (float, int)):  # type: ignore
        expected = "expected type 'float' or 'int'"
        actual = f"got {type(__value)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)

    result = datetime.datetime.fromtimestamp(__value).date()
    return result


DEFAULT_CONVERSIONS: Dict[type, Callable[..., Optional[datetime.date]]] = {
    datetime.date: date_from_date,
    datetime.datetime: date_from_datetime,
    decimal.Decimal: date_from_decimal,
    float: date_from_float,
    int: date_from_int,
    str: date_from_str,
}
