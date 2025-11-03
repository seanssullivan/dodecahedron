# -*- coding: utf-8 -*-
"""Abstract Converter.

Module defines an abstract class for converting values between data types.

"""

# Standard Library Imports
import abc
from typing import Any
from typing import Callable

__all__ = ["AbstractConverter"]


class AbstractConverter(abc.ABC):
    """Class represents an abstract converter."""

    @abc.abstractmethod
    def __call__(self, __value: Any, /) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def set_conversion(
        self, __type: type, func: Callable[..., Any], /
    ) -> None:
        """Set conversion for type.

        Args:
            __type: Type.
            func: Function for converting between types.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset converter."""
        raise NotImplementedError
