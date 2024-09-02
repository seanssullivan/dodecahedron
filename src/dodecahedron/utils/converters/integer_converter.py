# -*- coding: utf-8 -*-
"""Integer Converter.

Module provides function for converting values to integers.

"""

# Standard Library Imports
import datetime
import time
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_integer"]


class IntegerConverter(AbstractConverter):
    """Class implements a integer converter.

    Args:
        default (optional): Default value. Default ``0``.

    """

    def __init__(self, *, default: int = 0) -> None:
        if not isinstance(default, int):
            message = f"expected type 'int', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(self, __value: typing.Any, /) -> int:
        if __value is None:
            return self.default

        if isinstance(__value, bool):
            return self.from_bool(__value)

        if isinstance(__value, datetime.datetime):
            return self.from_datetime(__value)

        if isinstance(__value, datetime.date):
            return self.from_date(__value)

        if isinstance(__value, float):
            return self.from_float(__value)

        if isinstance(__value, int):
            return self.from_int(__value)

        if isinstance(__value, str):
            return self.from_str(__value)

        raise TypeError(f"{type(__value)} cannot be converted to int")

    def from_bool(self, __value: bool, /) -> int:
        """Convert boolean value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        result = int(__value)
        return result

    def from_date(self, __value: datetime.date, /) -> int:
        """Convert date value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        timestamp = time.mktime(__value.timetuple())
        result = int(timestamp)
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> int:
        """Convert datetime value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        timestamp = __value.timestamp()
        result = int(timestamp)
        return result

    def from_float(self, __value: float, /) -> int:
        """Convert float value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = int(__value)
        return result

    def from_int(self, __value: int, /) -> int:
        """Convert integer value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = int(__value)
        return result

    def from_str(self, __value: str, /) -> int:
        """Convert string value to ``int``.

        Args:
            __value: Value to convert to ``int``.

        Returns:
            Integer.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to ``int``.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.replace("  ", " ").strip()
        if not value:
            return self.default

        try:
            result = int(float(value))
        except ValueError:
            message = f"{__value} cannot be converted to int"
            raise ValueError(message)
        else:
            return result


def to_integer(__value: typing.Any, /, default: int = 0) -> int:
    """Convert value to integer.

    Args:
        __value: Value to convert to integer.
        default (optional): Default value. Default ``0``.

    Returns:
        Integer.

    """
    converter = IntegerConverter(default=default)
    result = converter(__value)
    return result
