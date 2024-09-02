# -*- coding: utf-8 -*-
"""Base Dispatcherr."""

# Local Imports
from .abstract_dispatcher import AbstractDispatcher
from ..messagebus import AbstractMessageBus

__all__ = ["BaseDispatcher"]


class BaseDispatcher(AbstractDispatcher):
    """Implements a base class for dispatchers to inherit."""

    def __init__(self, __bus: AbstractMessageBus, /) -> None:
        self._messagebus = __bus

    @property
    def messagebus(self) -> AbstractMessageBus:
        """Message bus."""
        return self._messagebus
