# -*- coding: utf-8 -*-
"""Datetime Converter.

Module provides function for converting values to datatimes.

"""

# Standard Library Imports
import datetime
import decimal
import logging
import operator
import typing

# Third-Party Imports
import cachetools
from cachetools.keys import hashkey
from dateutil.parser import parse
from dateutil.parser import ParserError
from dateutil.tz import tzlocal
import pytz

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_datetime"]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Getters
get_cache = operator.attrgetter("_cache")


class DatetimeConverter(AbstractConverter):
    """Class implements a datetime converter.

    Args:
        default (optional): Default value. Default ``None``.
        timezone (optional): Timezone. Default ``None``.

    """

    def __init__(
        self,
        *,
        default: typing.Optional[datetime.datetime] = None,
        timezone: typing.Optional[typing.Union[str, datetime.tzinfo]] = None,
    ) -> None:
        if default and not isinstance(default, datetime.datetime):
            message = f"expected type 'datetime', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)
        self._timezone = timezone
        self._cache = cachetools.LRUCache(maxsize=1000)

    @property
    def default(self) -> typing.Optional[datetime.datetime]:
        """Default."""
        result = (
            self._add_timezone(self._default)
            if isinstance(self._default, datetime.datetime)
            else self._default
        )
        return result

    def __call__(
        self, __value: typing.Any, /
    ) -> typing.Optional[datetime.datetime]:
        if __value is None:
            return self.default

        if isinstance(__value, datetime.datetime):
            return self.from_datetime(__value)

        if isinstance(__value, datetime.date):
            return self.from_date(__value)

        if isinstance(__value, decimal.Decimal):
            return self.from_decimal(__value)

        if isinstance(__value, float):
            return self.from_float(__value)

        if isinstance(__value, int):
            return self.from_int(__value)

        if isinstance(__value, str):
            return self.from_str(__value)

        raise TypeError(f"{type(__value)} cannot be converted to datetime")

    def from_bool(self, __value: bool, /) -> datetime.datetime:
        """Convert boolean value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        raise TypeError("'bool' cannot be converted to datetime")

    def from_date(self, __value: datetime.date, /) -> datetime.datetime:
        """Convert date value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Date.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        time = datetime.datetime.min.time()
        dt = datetime.datetime.combine(__value, time)
        result = self._add_timezone(dt)
        return result

    def from_datetime(
        self, __value: datetime.datetime, /
    ) -> datetime.datetime:
        """Convert datetime value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        dt = datetime.datetime(
            __value.year,
            __value.month,
            __value.day,
            __value.hour,
            __value.minute,
            __value.second,
            __value.microsecond,
            __value.tzinfo,
        )
        result = self._add_timezone(dt)
        return result

    def from_decimal(self, __value: decimal.Decimal, /) -> datetime.datetime:
        """Convert decimal value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        if not isinstance(__value, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(__value)} instead"
            raise TypeError(message)

        result = self.from_float(float(__value))
        return result

    def from_float(self, __value: float, /) -> datetime.datetime:
        """Convert float value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        try:
            dt = self._from_serial_date(__value)
        except ValueError:
            dt = self._from_timestamp(__value)

        result = self._add_timezone(dt)
        return result

    def _from_serial_date(self, __value: float, /) -> datetime.datetime:
        """Convert serial date value to ``datetime``.

        Implementation based on reply to a question on Stack Overflow.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        .. _Stack Overflow:
            https://stackoverflow.com/a/6706556/16732779

        """
        seconds = (__value - 25569) * 86400.0
        result = self._from_timestamp(seconds)
        return result

    def from_int(self, __value: int, /) -> datetime.date:
        """Convert integer value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        dt = self._from_timestamp(__value)
        result = self._add_timezone(dt)
        return result

    def _from_timestamp(
        self, __value: typing.Union[float, int], /
    ) -> datetime.datetime:
        """Convert timestamp value to ``datetime``.

        Args:
            __value: Value to convert to ``datetime``.

        Returns:
            Datetime.

        """
        result = datetime.datetime.fromtimestamp(__value)
        return result

    @cachetools.cachedmethod(get_cache, hashkey)
    def from_str(self, __value: str, /) -> datetime.datetime:
        """Convert string value to ``datetime``.

        Args:
            __value: String representation of datetime.

        Returns:
            Datetime.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to ``datetime``.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        try:
            value = __value.replace("  ", " ").strip()
            dt = parse(value) if value else self.default

        except (ParserError, ValueError):
            log.warn("Cannot convert '%s' to datetime", __value)
            dt = self.default

        result = self._add_timezone(dt)
        return result

    def _add_timezone(
        self, __datetime: datetime.datetime
    ) -> datetime.datetime:
        """Add timezone.

        Args:
            __datetime: Datetime.

        Returns:
            Datetime.

        """
        if self._timezone is None:
            return __datetime

        if isinstance(self._timezone, str) and is_naive(__datetime):
            result = pytz.timezone(self._timezone).localize(__datetime)
            return result

        result = __datetime.astimezone(self._timezone)
        return result


def to_datetime(
    __value: typing.Any,
    /,
    default: typing.Optional[datetime.datetime] = None,
    timezone: typing.Optional[typing.Union[str, datetime.tzinfo]] = tzlocal(),
) -> typing.Optional[datetime.datetime]:
    """Convert value to ``datetime``.

    Args:
        __value: Value to convert to ``datetime``.
        default (optional): Default value. Default ``None``.
        timezone (optional): Timezone. Default `local`.

    Returns:
        Datetime.

    """
    converter = DatetimeConverter(default=default, timezone=timezone)
    result = converter(__value)
    return result


# ----------------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------------
def is_naive(__dt: datetime.datetime) -> bool:
    """Check whether datetime is naive.

    Args:
        __dt: Datetime.

    Returns:
        Wether datetime is naive.

    """
    result = __dt.tzinfo is None or __dt.tzinfo.utcoffset(__dt) is None
    return result
