# -*- coding: utf-8 -*-
"""Abstract Dispatcherr."""

# Standard Library Imports
import abc

# Local Imports
from ..messagebus import AbstractMessageBus

__all__ = ["AbstractDispatcher"]


class AbstractDispatcher(abc.ABC):
    """Represents an abstract dispatcherr."""

    @property
    @abc.abstractmethod
    def messagebus(self) -> AbstractMessageBus:
        """Message bus."""
        raise NotImplementedError
