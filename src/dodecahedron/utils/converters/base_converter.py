# -*- coding: utf-8 -*-
"""Base Converter.

Module defines a base class for converting values between data types.

"""

# Standard Library Imports
from collections import ChainMap
from typing import Any
from typing import Callable
from typing import Literal
from typing import Type
from typing import TypeVar

# Local Imports
from .abstract_converter import AbstractConverter

__all__ = ["BaseConverter"]


# Custom type
T = TypeVar("T")


class BaseConverter(AbstractConverter):
    """Implements a base class for converters.

    Args:
        default (optional): Default value. Default ``None``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    _conversions: ChainMap[Type[Any], Callable[..., Any]]

    def __init__(
        self,
        *,
        default: Any = None,
        on_error: Literal["default", "raise"] = "raise",
    ) -> None:
        self._conversions = ChainMap()
        self._default = default

        if on_error not in ("default", "raise"):
            message = "invalid value for 'on_error' argument"
            raise ValueError(message)

        self._on_error = on_error

    @property
    def default(self) -> Any:
        """Default value."""
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = value

    def __call__(self, __value: Any, /) -> Any:
        try:
            result = (
                self._handle_conversion(__value)
                if __value is not None
                else self._default
            )
        except KeyError as error:
            result = self._handle_exception(__value, error)

        return result

    def _handle_conversion(self, __value: Any, /) -> Any:
        """Handle conversion between data types.

        Args:
            __value: Value to convert.

        Returns:
            Converted value.

        """
        conversion = self._conversions[type(__value)]
        result = conversion(__value, self._default)
        return result

    def _handle_exception(self, __value: Any, error: Exception, /) -> Any:
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

    def set_conversion(
        self, __type: type, func: Callable[..., Any], /
    ) -> None:
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
