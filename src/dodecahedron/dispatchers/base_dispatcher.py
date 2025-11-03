# -*- coding: utf-8 -*-
"""Base Dispatcherr."""

# Local Imports
from .abstract_dispatcher import AbstractDispatcher
from ..messagebus import AbstractMessageBus

__all__ = ["BaseDispatcher"]


class BaseDispatcher(AbstractDispatcher):
    """Implements a base class for dispatchers to inherit.

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
