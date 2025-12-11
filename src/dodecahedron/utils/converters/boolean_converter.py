# -*- coding: utf-8 -*-
"""Boolean Converter.

Module provides function for converting values to booleans.

"""

# Standard Library Imports
import datetime
import decimal
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_boolean"]


# Constants
FALSY_VALUES = ("false", "no", "n", "0")
TRUTHY_VALUES = ("true", "yes", "y", "1")


def to_boolean(__value: Any, /, default: bool = False) -> bool:
    """Convert value to boolean.

    Args:
        __value: Value to convert to boolean.
        default (optional): Default value. Default ``False``.

    Returns:
        Boolean.

    """
    converter = BooleanConverter(default=default)
    result = converter(__value)
    return result


class BooleanConverter(BaseConverter):
    """Class implements a boolean converter.

    Args:
        default (optional): Default value. Default ``False``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: bool = False,
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, bool):  # type: ignore
            message = f"expected type 'bool', got {type(default)} instead"
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
        if not isinstance(value, bool):  # type: ignore
            message = f"expected type 'bool', got {type(value)} instead"
            raise TypeError(message)

        self._default = value


def bool_from_bool(__value: bool, _: bool, /) -> bool:
    """Convert boolean value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):  # type: ignore  # pragma: no cover
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_date(__value: datetime.date, _: bool, /) -> bool:
    """Convert date value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):  # type: ignore  # pragma: no cover
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_datetime(__value: datetime.datetime, _: bool, /) -> bool:
    """Convert datetime value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):  # type: ignore  # pragma: no cover
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_decimal(__value: decimal.Decimal, _: bool, /) -> bool:
    """Convert decimal value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):  # type: ignore  # pragma: no cover
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_float(__value: float, _: bool, /) -> bool:
    """Convert float value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):  # type: ignore  # pragma: no cover
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_int(__value: int, _: bool, /) -> bool:
    """Convert integer value to ``bool``.

    Args:
        __value: Value to convert to ``bool``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):  # type: ignore  # pragma: no cover
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = bool(__value)
    return result


def bool_from_str(__value: str, default: bool = False, /) -> bool:
    """Convert string value to `bool`.

    Args:
        __value: Value to convert to ``bool``.
        default (optional): Default value. Default ``False``.

    Returns:
        Boolean.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to ``bool``.

    """
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    if value.lower() in TRUTHY_VALUES:
        return True

    if value.lower() in FALSY_VALUES:
        return False

    raise ValueError(f"'{__value}' cannot be converted to bool")


DEFAULT_CONVERSIONS: Dict[type, Callable[..., bool]] = {
    bool: bool_from_bool,
    datetime.date: bool_from_date,
    datetime.datetime: bool_from_datetime,
    decimal.Decimal: bool_from_decimal,
    float: bool_from_float,
    int: bool_from_int,
    str: bool_from_str,
}
