# -*- coding: utf-8 -*-
"""Abstract Progress Bar."""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Optional
from typing import Union

__all__ = ["AbstractProgressBar"]


class AbstractProgressBar(abc.ABC):
    """Represents an abstract progress bar."""

    @property
    @abc.abstractmethod
    def current(self) -> int:
        """Current progress."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def leave(self) -> bool:
        """Whether progress bar is maintained between iterations."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def total(self) -> int:
        """Total progress."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Close progress bar."""
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        """Refresh progress bar."""
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self, total: Optional[Union[float, int]] = None) -> None:
        """Reset progress bar."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self) -> None:
        """Update progress bar."""
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, message: str) -> None:
        """Write message to progress bar."""
        raise NotImplementedError
