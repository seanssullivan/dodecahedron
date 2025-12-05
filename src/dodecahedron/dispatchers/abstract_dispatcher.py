# -*- coding: utf-8 -*-
"""Abstract Dispatcherr."""

# Standard Library Imports
import abc

# Local Imports
from ..messagebus import AbstractMessageBus

__all__ = ["AbstractDispatcher"]


class AbstractDispatcher(abc.ABC):
    """Class represents an abstract dispatcherr.

    Args:
        __bus: Message bus.

    Attributes:
        messagebus: Message bus.

    Raises:
        TypeError: when argument is not type ``AbstractMessageBus``.

    """

    def __init__(self, __bus: AbstractMessageBus, /) -> None:
        if not isinstance(__bus, AbstractMessageBus):  # type: ignore
            expected = "expected type 'AbstractMessageBus'"
            actual = f"got {type(__bus)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._messagebus = __bus

    @property
    def messagebus(self) -> AbstractMessageBus:
        """Message bus."""
        return self._messagebus
