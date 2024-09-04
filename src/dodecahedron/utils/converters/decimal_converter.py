# -*- coding: utf-8 -*-
"""Decimal Converter.

Module provides function for converting values to decimals.

"""

# Standard Library Imports
import datetime
import decimal
import re
import time
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_decimal"]


class DecimalConverter(AbstractConverter):
    """Class implements a decimal converter.

    Args:
        default (optional): Default value. Default ``0.0``.

    """

    def __init__(
        self, *, default: decimal.Decimal = decimal.Decimal("0.0")
    ) -> None:
        if not isinstance(default, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(self, __value: typing.Any, /) -> decimal.Decimal:
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

        raise TypeError(f"{type(__value)} cannot be converted to decimal")

    def from_bool(self, __value: bool, /) -> decimal.Decimal:
        """Convert boolean value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        result = decimal.Decimal(__value)
        return result

    def from_date(self, __value: datetime.date, /) -> decimal.Decimal:
        """Convert date value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        value = time.mktime(__value.timetuple())
        result = decimal.Decimal(str(value))
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> decimal.Decimal:
        """Convert datetime value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.timestamp()
        result = decimal.Decimal(str(value))
        return result

    def from_decimal(self, __value: decimal.Decimal, /) -> decimal.Decimal:
        """Convert decimal value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(__value)} instead"
            raise TypeError(message)

        result = decimal.Decimal(__value)
        return result

    def from_float(self, __value: float, /) -> decimal.Decimal:
        """Convert float value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = decimal.Decimal(str(__value))
        return result

    def from_int(self, __value: int, /) -> decimal.Decimal:
        """Convert integer value to decimal.

        Args:
            __value: Value to convert to decimal.

        Returns:
            Decimal.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = decimal.Decimal(__value)
        return result

    def from_str(self, __value: str, /) -> decimal.Decimal:
        """Convert string value to decimal.

        Args:
            __value: String representation of decimal value.

        Returns:
            Decimal.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to decimal.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.replace("  ", " ").strip()
        if not value:
            return self.default

        try:
            result = decimal.Decimal(re.sub(r"[^0-9a-zA-Z.]+", r"", value))
        except decimal.InvalidOperation:
            raise ValueError(f"'{__value}' cannot be converted to decimal")
        else:
            return result


def to_decimal(
    __value: typing.Any, /, default: decimal.Decimal = decimal.Decimal("0.0")
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
