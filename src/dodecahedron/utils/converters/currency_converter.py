# -*- coding: utf-8 -*-
"""Currency Converter.

Module provides function for converting values to currencies.

"""

# Standard Library Imports
import decimal
import re
import typing

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_currency"]


def to_currency(__value: typing.Any, /, default: float = 0.00) -> float:
    """Convert value to currency.

    Args:
        __value: Value to convert to currency.
        default (optional): Default value. Default ``0.00``.

    Returns:
        Amount.

    """
    converter = CurrencyConverter(default=default)
    result = converter(__value)
    return result


class CurrencyConverter(BaseConverter):
    """Class implements a currency converter.

    Args:
        default (optional): Default value. Default ``0.00``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: float = 0.00,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def currency_from_decimal(__value: decimal.Decimal, _: float, /) -> float:
    """Convert decimal value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = float(round(__value, 2))
    return result


def currency_from_float(__value: float, _: float, /) -> float:
    """Convert float value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = round(__value, 2)
    return result


def currency_from_int(__value: int, _: float, /) -> float:
    """Convert integer value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = round(float(__value), 2)
    return result


def currency_from_str(__value: str, default: float = 0.00, /) -> float:
    """Convert string value to currency.

    Args:
        __value: String representation of currency value.
        default (optional): Default value. Default ``0.00``.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to currency.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        amount = float(re.sub(r"[^0-9a-zA-Z.]+", r"", value))
    except ValueError:
        message = f"'{__value}' cannot be converted to currency"
        raise ValueError(message)
    else:
        result = round(amount, 2)
        return result


DEFAULT_CONVERSIONS = {
    decimal.Decimal: currency_from_decimal,
    float: currency_from_float,
    int: currency_from_int,
    str: currency_from_str,
}  # type: typing.Dict[type, typing.Callable]
