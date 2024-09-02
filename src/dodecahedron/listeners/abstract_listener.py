# -*- coding: utf-8 -*-

# Standard Imports
import abc

__all__ = ["AbstractListener"]


class AbstractListener(abc.ABC):
    """Represents an abstract listener."""

    @abc.abstractmethod
    def start(self) -> None:
        """Start listener."""
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self) -> None:
        """Stop listener."""
        raise NotImplementedError
