# -*- coding: utf-8 -*-
"""Abstract Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
from typing import Any
from typing import Hashable
from typing import List
from typing import Set

# Local Imports
from ..metaclasses import RepositoryMeta
from ..metaclasses.tracker import SEEN_ATTR

__all__ = ["AbstractRepository"]


class AbstractRepository(abc.ABC, metaclass=RepositoryMeta):
    """Represents an abstract repository."""

    @property
    def seen(self) -> Set[Any]:
        """Objects seen."""
        return getattr(self, SEEN_ATTR, set())

    @abc.abstractmethod
    def add(self, obj: Any, /, *args: Any, **kwargs: Any) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: Hashable, /, *args: Any, **kwargs: Any) -> Any:
        """Get object from repository.

        Args:
            ref: Reference to object.
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        Returns:
            Object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, /, *args: Any, **kwargs: Any) -> List[Any]:
        """List objects in repository.

        Args:
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        Returns:
            Objects.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: Any, /, *args: Any, **kwargs: Any) -> None:
        """Remove object from repository.

        Args:
            obj: Object to remove from repository.
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self, *args: Any, **kwargs: Any) -> None:
        """Commit changes to repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self, *args: Any, **kwargs: Any) -> None:
        """Rollback changes to repository."""
        raise NotImplementedError
