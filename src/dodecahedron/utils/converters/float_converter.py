# -*- coding: utf-8 -*-
"""Float Converter.

Module provides functions for converting values to floats.

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

__all__ = ["to_float"]


def to_float(
    __value: Any,
    /,
    default: Optional[float] = 0.0,
) -> Optional[float]:
    """Convert value to float.

    Args:
        __value: Value to convert to float.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Float.

    """
    converter = FloatConverter(default=default)
    result = converter(__value)
    return result


class FloatConverter(BaseConverter):
    """Class implements a float converter.

    Args:
        default (optional): Default value. Default ``0.0``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: Optional[float] = 0.0,
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        if default is not None and not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
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
        if not isinstance(value, float):  # type: ignore
            message = f"expected type 'float', got {type(value)} instead"
            raise TypeError(message)

        self._default = value


def float_from_bool(__value: bool, /, *_: Any) -> float:
    """Convert boolean value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):  # type: ignore  # pragma: no cover
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def float_from_date(__value: datetime.date, /, *_: Any) -> float:
    """Convert date value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):  # type: ignore  # pragma: no cover
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = time.mktime(__value.timetuple())
    return result


def float_from_datetime(__value: datetime.datetime, /, *_: Any) -> float:
    """Convert datetime value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):  # type: ignore  # pragma: no cover
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = __value.timestamp()
    return result


def float_from_decimal(__value: decimal.Decimal, /, *_: Any) -> float:
    """Convert decimal value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):  # type: ignore  # pragma: no cover
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def float_from_float(__value: float, /, *_: Any) -> float:
    """Convert float value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):  # type: ignore  # pragma: no cover
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def float_from_int(__value: int, /, *_: Any) -> float:
    """Convert integer value to float.

    Args:
        __value: Value to convert to float.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):  # type: ignore  # pragma: no cover
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def float_from_str(
    __value: str,
    /,
    default: Optional[float] = 0.0,
) -> Optional[float]:
    """Convert string value to float.

    Args:
        __value: String representation of float value.

    Returns:
        Float.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to float.

    """
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        result = parsers.parse_number(value) if value else default

    except ValueError:
        message = f"{type(__value)} cannot be converted to float"
        raise ValueError(message)

    return result


DEFAULT_CONVERSIONS: Dict[type, Callable[..., Optional[float]]] = {
    bool: float_from_bool,
    datetime.date: float_from_date,
    datetime.datetime: float_from_datetime,
    decimal.Decimal: float_from_decimal,
    float: float_from_float,
    int: float_from_int,
    str: float_from_str,
}
