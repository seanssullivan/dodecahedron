# -*- coding: utf-8 -*-
"""Base Converter.

Module defines a base class for converting values between data types.

"""

# Standard Library Imports
import collections
import typing

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["BaseConverter"]


# Custom type
T = typing.TypeVar("T")


class BaseConverter(AbstractConverter):
    """Implements a base class for converters.

    Args:
        default (optional): Default value. Default ``None``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: typing.Any = None,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        self._conversions = collections.ChainMap()
        self._default = default

        if on_error not in ("default", "raise"):
            message = "invalid value for 'on_error' argument"
            raise ValueError(message)

        self._on_error = on_error

    def __call__(self, __value: typing.Any, /) -> typing.Any:
        try:
            result = (
                self._handle_conversion(__value)
                if __value is not None
                else self._default
            )
        except KeyError as error:
            result = self._handle_exception(__value, error)

        return result

    def _handle_conversion(self, __value: typing.Any, /) -> typing.Any:
        """Handle conversion between data types.

        Args:
            __value: Value to convert.

        Returns:
            Converted value.

        """
        conversion = self._conversions[type(__value)]
        result = conversion(__value, self._default)
        return result

    def _handle_exception(
        self, __value: typing.Any, error: Exception, /
    ) -> typing.Any:
        """Handle conversion between data types.

        Args:
            __value: Value to convert.

        Returns:
            Converted value.

        """
        if self._on_error == "raise":
            message = f"unable to convert from {type(__value)}"
            raise TypeError(message) from error

        return self._default

    def set_conversion(self, __type: type, func: typing.Callable, /) -> None:
        """Set conversion for type.

        Args:
            __type: Type.
            func: Function for converting between types.

        """
        self._conversions[__type] = func

    def reset(self) -> None:
        """Reset converter."""
        self._conversions = (
            self._conversions.parents
            if len(self._conversions.maps) > 1
            else self._conversions
        )
