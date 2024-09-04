# -*- coding: utf-8 -*-
"""String Converter.

Module provides function for converting values to strings.

"""

# Standard Library Imports
import datetime
import decimal
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["to_string"]


class StringConverter(AbstractConverter):
    """Class implements a string converter.

    Args:
        default (optional): Default value. Default ``None``.

    """

    _date_format: str = "%Y-%m-%d"
    _datetime_format: str = "%Y-%m-%d %H:%M:%S"
    _decimal_points: typing.Union[float, int] = float("inf")

    def __init__(self, *, default: typing.Optional[str] = None) -> None:
        if default and not isinstance(default, str):
            message = f"expected type 'str', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default)

    @classmethod
    def set_date_format(cls, __format: str, /) -> None:
        """Set format when converting date values to strings.

        Args:
            __format: Date format.

        """
        if not isinstance(__format, str):
            message = f"expected type 'str', got {type(__format)} instead"
            raise TypeError(message)

        cls._date_format = __format

    @classmethod
    def set_datetime_format(cls, __format: str, /) -> None:
        """Set format when converting datetime values to strings.

        Args:
            __format: Datetime format.

        """
        if not isinstance(__format, str):
            message = f"expected type 'str', got {type(__format)} instead"
            raise TypeError(message)

        cls._datetime_format = __format

    @classmethod
    def set_decimal_points(cls, n: int, /) -> None:
        """Set decimal points when converting float values to strings.

        Args:
            n: Number of decimal points.

        """
        cls._decimal_points = n

    def __call__(self, __value: typing.Any, /) -> int:
        if __value is None:
            return self.default

        if isinstance(__value, bool):
            return self.from_bool(__value)

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

        raise TypeError(f"{type(__value)} cannot be converted to str")

    def from_bool(self, __value: bool, /) -> str:
        """Convert boolean value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, bool):
            message = f"expected type 'bool', got {type(__value)} instead"
            raise TypeError(message)

        result = str(__value)
        return result

    def from_date(self, __value: datetime.date, /) -> str:
        """Convert date value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, datetime.date):
            message = f"expected type 'date', got {type(__value)} instead"
            raise TypeError(message)

        result = (
            __value.strftime(self._date_format)
            if self._date_format
            else str(__value)
        )
        return result

    def from_datetime(self, __value: datetime.datetime, /) -> str:
        """Convert datetime value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, datetime.datetime):
            message = f"expected type 'datetime', got {type(__value)} instead"
            raise TypeError(message)

        result = (
            __value.strftime(self._datetime_format)
            if self._datetime_format
            else str(__value)
        )
        return result

    def from_decimal(self, __value: decimal.Decimal, /) -> int:
        """Convert decimal value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, decimal.Decimal):
            message = f"expected type 'Decimal', got {type(__value)} instead"
            raise TypeError(message)

        result = self.from_float(float(__value))
        return result

    def from_float(self, __value: float, /) -> str:
        """Convert float value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, float):
            message = f"expected type 'float', got {type(__value)} instead"
            raise TypeError(message)

        value = (
            round(__value, self._decimal_points)
            if self._decimal_points < float("inf")
            else __value
        )
        result = str(value)
        return result

    def from_int(self, __value: int, /) -> str:
        """Convert integer value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        """
        if not isinstance(__value, int):
            message = f"expected type 'int', got {type(__value)} instead"
            raise TypeError(message)

        result = str(__value)
        return result

    def from_str(self, __value: str, /) -> str:
        """Convert string value to ``str``.

        Args:
            __value: Value to convert to ``str``.

        Returns:
            String.

        Raises:
            TypeError: when value is not type 'str'.
            ValueError: when value cannot be converted to ``str``.

        """
        if not isinstance(__value, str):
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        value = __value.replace("  ", " ").strip()
        if not value:
            return self.default

        result = str(__value)
        return result


def to_string(
    __value: object, /, default: typing.Optional[str] = None
) -> typing.Optional[str]:
    """Convert value to string.

    Args:
        value: Value to convert.

    Returns:
        String.

    """
    converter = StringConverter(default=default)
    result = converter(__value)
    return result
