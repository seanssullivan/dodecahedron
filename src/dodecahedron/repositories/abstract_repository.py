# -*- coding: utf-8 -*-
"""Abstract Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
import typing

# Local Imports
from ..metaclasses import RepositoryMeta
from ..metaclasses.tracker import SEEN_ATTR

__all__ = ["AbstractRepository"]


class AbstractRepository(abc.ABC, metaclass=RepositoryMeta):
    """Represents an abstract repository."""

    @property
    def seen(self) -> set:
        """Objects seen."""
        return getattr(self, SEEN_ATTR, set())

    @abc.abstractmethod
    def add(self, obj: typing.Any) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: typing.Union[int, str]) -> typing.Any:
        """Get object from repository.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list:
        """List objects in repository.

        Returns:
            Objects in repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: typing.Any) -> None:
        """Remove object from repository.

        Args:
            obj: Object to remove from repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit changes to repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback changes to repository."""
        raise NotImplementedError
