# -*- coding: utf-8 -*-
"""Date Converter.

Module provides function for converting values to dates.

"""

# Standard Library Imports
import datetime
import logging
import typing

# Third-Party Imports
import cachetools
from cachetools.keys import hashkey
from dateutil.parser import parse
from dateutil.parser import ParserError

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_date"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


class DateConverter(AbstractConverter):
    """Class implements a date converter.

    Args:
        default (optional): Default value. Default ``None``.

    """

    def __init__(
        self, *, default: typing.Optional[datetime.date] = None
    ) -> None:
        if default and not isinstance(default, datetime.date):
            message = f"expected type 'date', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    def __call__(
        self, __value: typing.Any, /
    ) -> typing.Optional[datetime.date]:
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

        raise TypeError(f"{type(__value)} cannot be converted to date")

    def from_bool(self, __value: bool, /) -> datetime.date:
        """Convert boolean value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'bool' cannot be converted to date")

    def from_date(self, __value: datetime.date, /) -> datetime.date:
        """Convert date value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        result = datetime.date(__value.year, __value.month, __value.day)
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> datetime.date:
        """Convert datetime value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        result = __value.date()
        return result

    def from_float(self, __value: float, /) -> datetime.date:
        """Convert float value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        # TODO: Determine whether value is a serial date.
        result = self._from_serial_date(__value)
        return result

    def _from_serial_date(self, __value: float, /) -> datetime.date:
        """Convert serial date value to ``date``.

        Implementation based on reply to a question on Stack Overflow.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        .. _Stack Overflow:
            https://stackoverflow.com/a/6706556/16732779

        """
        seconds = (__value - 25569) * 86400.0
        result = self._from_timestamp(seconds)
        return result

    def from_int(self, __value: int, /) -> datetime.date:
        """Convert integer value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = self._from_timestamp(__value)
        return result

    def _from_timestamp(self, __value: int, /) -> datetime.date:
        """Convert timestamp value to ``date``.

        Args:
            __value: Value to convert to ``date``.

        Returns:
            Date.

        """
        dt = datetime.datetime.fromtimestamp(__value)
        result = self.from_datetime(dt)
        return result

    @cachetools.cachedmethod(cachetools.LRUCache(maxsize=1000), hashkey)
    def from_str(self, __value: str, /) -> datetime.date:
        """Convert string value to ``date``.

        Args:
            __value: String representation of date.

        Returns:
            Date.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to ``date``.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        try:
            value = __value.replace("  ", " ").strip()
            result = parse(value).date() if value else self.default

        except (ParserError, ValueError):
            log.warn("Cannot convert '%s' to date", __value)
            result = self.default

        return result


def to_date(
    __value: typing.Any, /, default: typing.Optional[datetime.date] = None
) -> typing.Optional[datetime.date]:
    """Converts value to date.

    Args:
        __value: Date.
        default (optional): Default value. Default ``None``.

    Returns:
        Date.

    """
    converter = DateConverter(default=default)
    result = converter(__value)
    return result
