# -*- coding: utf-8 -*-
"""Currency Converter.

Module provides function for converting values to currencies.

"""

# Standard Library Imports
import decimal
import re
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal
from typing import Optional
from typing import overload

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_currency"]


@overload
def to_currency(
    __value: Any,
    /,
    default: float,
) -> float: ...


@overload
def to_currency(
    __value: Any,
    /,
    default: Optional[float] = None,
) -> Optional[float]: ...


def to_currency(
    __value: Any,
    /,
    default: Optional[float] = 0.00,
) -> Optional[float]:
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
        default: Optional[float] = 0.00,
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


def currency_from_decimal(__value: decimal.Decimal, /, *_: Any) -> float:
    """Convert decimal value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):  # type: ignore  # pragma: no cover
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = float(round(__value, 2))
    return result


def currency_from_float(__value: float, /, *_: Any) -> float:
    """Convert float value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):  # type: ignore  # pragma: no cover
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = round(__value, 2)
    return result


def currency_from_int(__value: int, /, *_: Any) -> float:
    """Convert integer value to currency.

    Args:
        __value: Value to convert to currency.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):  # type: ignore  # pragma: no cover
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = round(float(__value), 2)
    return result


def currency_from_str(
    __value: str,
    /,
    default: Optional[float] = 0.00,
) -> Optional[float]:
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
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        amount = re.sub(r"[^0-9a-zA-Z.]+", r"", value) if value else default
        result = round(float(amount), 2) if amount is not None else None

    except ValueError:
        message = f"'{__value}' cannot be converted to currency"
        raise ValueError(message)

    return result


DEFAULT_CONVERSIONS: Dict[type, Callable[..., Optional[float]]] = {
    decimal.Decimal: currency_from_decimal,
    float: currency_from_float,
    int: currency_from_int,
    str: currency_from_str,
}
