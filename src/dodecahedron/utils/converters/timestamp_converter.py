# -*- coding: utf-8 -*-
"""Timestamp Converter.

Module provides function for converting values to timestamps.

"""

# Standard Library Imports
import datetime
import logging
import time
import typing

# Third-Party Imports
from dateutil.parser import parse
from dateutil.parser import ParserError

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_timestamp"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


class TimestampConverter(AbstractConverter):
    """Class implements a timestamp converter.

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
        """Convert boolean value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'bool' cannot be converted to timestamp")

    def from_date(self, __value: datetime.date, /) -> int:
        """Convert date value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        result = time.mktime(__value.timetuple())
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> int:
        """Convert datetime value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        result = __value.timestamp()
        return result

    def from_float(self, __value: float, /) -> int:
        """Convert float value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        result = float(__value)
        return result

    def from_int(self, __value: int, /) -> int:
        """Convert integer value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = float(__value)
        return result

    def from_str(self, __value: str, /) -> int:
        """Convert string value to timestamp.

        Args:
            __value: Value to convert to timestamp.

        Returns:
            Timestamp.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to timestamp.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        try:
            value = __value.replace("  ", " ").strip()
            result = parse(value).timestamp() if value else self.default

        except (ParserError, ValueError):
            log.warn("Cannot convert '%s' to timestamp", __value)
            result = self.default

        else:
            return result


def to_timestamp(__value: typing.Any, /, default: float = 0.0) -> float:
    """Convert date to timestamp.

    Args:
        __value: Value to convert to timestamp.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Timestamp.
    """
    converter = TimestampConverter(default=default)
    result = converter(__value)
    return result
