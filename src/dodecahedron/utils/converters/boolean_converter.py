# -*- coding: utf-8 -*-
"""Boolean Converter.

Module provides function for converting values to booleans.

"""

# Standard Library Imports
import datetime
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_boolean"]


# Constants
FALSY_VALUES = ("false", "no", "n", "0")
TRUTHY_VALUES = ("true", "yes", "y", "1")


class BooleanConverter(AbstractConverter):
    """Class implements a boolean converter.

    Args:
        default (optional): Default value. Default ``False``.

    Todo:
        * Allow falsy and truthy values as arguments.

    """

    def __init__(self, *, default: bool = False) -> None:
        if not isinstance(default, bool):
            message = f"expected type 'bool', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(self, __value: typing.Any, /) -> bool:
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

        raise TypeError(f"{type(__value)} cannot be converted to bool")

    def from_bool(self, __value: bool, /) -> bool:
        """Convert boolean value to ``bool``.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        result = bool(__value)
        return result

    def from_date(self, __value: datetime.date, /) -> bool:
        """Convert date value to ``bool``.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        result = bool(__value)
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> bool:
        """Convert datetime value to ``bool``.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        result = bool(__value)
        return result

    def from_float(self, __value: float, /) -> bool:
        """Convert float value to ``bool``.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = self.from_int(int(__value))
        return result

    def from_int(self, __value: int, /) -> bool:
        """Convert integer value to ``bool``.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = bool(__value)
        return result

    def from_str(self, __value: str, /) -> bool:
        """Convert string value to `bool`.

        Args:
            __value: Value to convert to ``bool``.

        Returns:
            Boolean.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to ``bool``.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.replace("  ", " ").strip()
        if not value:
            return self.default

        if value.lower() in TRUTHY_VALUES:
            return True

        if value.lower() in FALSY_VALUES:
            return False

        raise ValueError(f"'{__value}' cannot be converted to bool")


def to_boolean(__value: typing.Any, /, default: bool = False) -> bool:
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
