# -*- coding: utf-8 -*-
"""String Converter.

Module provides function for converting values to strings.

"""

# Standard Library Imports
import datetime
import decimal
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal
from typing import Optional

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_string"]


def to_string(
    __value: object, /, default: Optional[str] = None
) -> Optional[str]:
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
        default: Optional[str] = None,
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        if default and not isinstance(default, str):  # type: ignore
            message = f"expected type 'str', got {type(default)} instead"
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
        if not isinstance(value, str):  # type: ignore
            message = f"expected type 'str', got {type(value)} instead"
            raise TypeError(message)

        self._default = value


def str_from_bool(__value: bool, _: Optional[str] = None, /) -> str:
    """Convert boolean value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'bool'.

    """
    if not isinstance(__value, bool):  # type: ignore  # pragma: no cover
        message = f"expected type 'bool', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_date(__value: datetime.date, _: Optional[str] = None, /) -> str:
    """Convert date value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, datetime.date):  # type: ignore  # pragma: no cover
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_datetime(
    __value: datetime.datetime, _: Optional[str] = None, /
) -> str:
    """Convert datetime value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime.datetime):  # type: ignore  # pragma: no cover
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_decimal(
    __value: decimal.Decimal, _: Optional[str] = None, /
) -> str:
    """Convert decimal value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):  # type: ignore  # pragma: no cover
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_float(__value: float, _: Optional[str] = None, /) -> str:
    """Convert float value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):  # type: ignore  # pragma: no cover
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_int(__value: int, _: Optional[str] = None, /) -> str:
    """Convert integer value to ``str``.

    Args:
        __value: Value to convert to ``str``.

    Returns:
        String.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):  # type: ignore  # pragma: no cover
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = str(__value)
    return result


def str_from_str(
    __value: str, default: Optional[str] = None, /
) -> Optional[str]:
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
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    result = str(__value)
    return result


DEFAULT_CONVERSIONS: Dict[type, Callable[..., Optional[str]]] = {
    bool: str_from_bool,
    datetime.date: str_from_date,
    datetime.datetime: str_from_datetime,
    decimal.Decimal: str_from_decimal,
    float: str_from_float,
    int: str_from_int,
    str: str_from_str,
}
