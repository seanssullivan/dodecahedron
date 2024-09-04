# -*- coding: utf-8 -*-
"""Currency Converter.

Module provides function for converting values to currencies.

"""

# Standard Library Imports
import datetime
import decimal
import re
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_currency"]


class CurrencyConverter(AbstractConverter):
    """Class implements a currency converter.

    Args:
        default (optional): Default value. Default ``0.00``.

    """

    def __init__(self, *, default: float = 0.0) -> None:
        if not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(self, __value: typing.Any, /) -> float:
        if __value is None:
            return self.default

        if isinstance(__value, decimal.Decimal):
            return self.from_decimal(__value)

        if isinstance(__value, float):
            return self.from_float(__value)

        if isinstance(__value, int):
            return self.from_int(__value)

        if isinstance(__value, str):
            return self.from_str(__value)

        raise TypeError(f"{type(__value)} cannot be converted to currency")

    def from_bool(self, __value: bool, /) -> float:
        """Convert boolean value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'bool' cannot be converted to currency")

    def from_date(self, __value: datetime.date, /) -> float:
        """Convert date value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'date' cannot be converted to currency")

    def from_datetime(self, __value: datetime.datetime, /) -> float:
        """Convert datetime value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'datetime' cannot be converted to currency")

    def from_decimal(self, __value: decimal.Decimal, /) -> float:
        """Convert decimal value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(__value)} instead"
            raise TypeError(message)

        result = float(round(__value, 2))
        return result

    def from_float(self, __value: float, /) -> float:
        """Convert float value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = round(__value, 2)
        return result

    def from_int(self, __value: int, /) -> float:
        """Convert integer value to currency.

        Args:
            __value: Value to convert to currency.

        Returns:
            Amount.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = self.from_float(float(__value))
        return result

    def from_str(self, __value: str, /) -> float:
        """Convert string value to currency.

        Args:
            __value: String representation of currency value.

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
            return self.default

        try:
            amount = float(re.sub(r"[^0-9a-zA-Z.]+", r"", value))
        except ValueError:
            message = f"'{__value}' cannot be converted to currency"
            raise ValueError(message)
        else:
            result = round(amount, 2)
            return result


def to_currency(__value: typing.Any, /, default: float = 0.0) -> float:
    """Convert value to currency.

    Args:
        __value: Value to convert to currency.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Amount.

    """
    converter = CurrencyConverter(default=default)
    result = converter(__value)
    return result
