# -*- coding: utf-8 -*-
"""Abstract Converter.

Module defines a class for converting values to boolean.

"""

# Standard Library Imports
import abc
import datetime
import decimal
import typing

__all__ = ["AbstractConverter"]


# Custom type
T = typing.TypeVar("T")


class AbstractConverter(abc.ABC):
    """Class represents an abstract converter."""

    def __init__(self, *, default: typing.Optional[T] = None) -> None:
        self._default = default

    @property
    def default(self) -> typing.Optional[T]:
        """Default."""
        return self._default

    @abc.abstractmethod
    def __call__(self, __value: typing.Any, /) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def from_bool(self, __value: bool, /) -> typing.Any:
        """Make value from boolean."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_date(self, __value: datetime.date, /) -> typing.Any:
        """Make value from date."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_datetime(self, __value: datetime.datetime, /) -> typing.Any:
        """Make value from datetime."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_decimal(self, __value: decimal.Decimal, /) -> typing.Any:
        """Make value from decimal."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_float(self, __value: float, /) -> typing.Any:
        """Make value from float."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_int(self, __value: int, /) -> typing.Any:
        """Make value from integer."""
        raise NotImplementedError

    @abc.abstractmethod
    def from_str(self, __value: str, /) -> typing.Any:
        """Make value from string."""
        raise NotImplementedError
