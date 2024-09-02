# -*- coding: utf-8 -*-
"""Distance Converter.

Module provides functions for converting values to distances.

"""

# Standard Library Imports
import datetime
import re
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_distance"]


class DistanceConverter(AbstractConverter):
    """Class implements a distance converter.

    Args:
        default (optional): Default value. Default ``0.0``.

    """

    def __init__(self, *, default: float = 0.0) -> None:
        if not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(self, __value: typing.Any, /) -> float:
        if __value is None:
            return self.default

        if isinstance(__value, float):
            return self.from_float(__value)

        if isinstance(__value, int):
            return self.from_int(__value)

        if isinstance(__value, str):
            return self.from_str(__value)

        raise TypeError(f"{type(__value)} cannot be converted to distance")

    def from_bool(self, __value: bool, /) -> float:
        """Convert boolean value to distance.

        Args:
            __value: Value to convert to distance.

        Returns:
            Distance.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'bool' cannot be converted to distance")

    def from_date(self, __value: datetime.date, /) -> bool:
        """Convert date value to distance.

        Args:
            __value: Value to convert to distance.

        Returns:
            Distance.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'date' cannot be converted to distance")

    def from_datetime(self, __value: datetime.datetime, /) -> bool:
        """Convert datetime value to distance.

        Args:
            __value: Value to convert to distance.

        Returns:
            Distance.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'datetime' cannot be converted to distance")

    def from_float(self, __value: float, /) -> float:
        """Convert float value to distance.

        Args:
            __value: Value to convert to distance.

        Returns:
            Distance.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = float(__value)
        return result

    def from_int(self, __value: int, /) -> float:
        """Convert integer value to distance.

        Args:
            __value: Value to convert to distance.

        Returns:
            Distance.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = self.from_float(float(__value))
        return result

    def from_str(self, __value: str, /) -> float:
        """Convert string value to distance.

        Args:
            __value: String representation of distance value.

        Returns:
            Distance.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to distance.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.replace("  ", " ").strip()
        if not value:
            return self.default

        try:
            pattern = r"(\d+),?(\d*.?\d*)\s?m?"
            replacement = r"\1\2"
            result = float(re.sub(pattern, replacement, value, flags=re.I))
        except ValueError:
            raise ValueError(
                f"{type(__value)} cannot be converted to distance"
            )
        else:
            return result


def to_distance(__value: typing.Any, /, default: float = 0.0) -> float:
    """Convert value to distance.

    Args:
        __value: Value to convert to distance.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Distance.

    """
    converter = DistanceConverter(default=default)
    result = converter(__value)
    return result
