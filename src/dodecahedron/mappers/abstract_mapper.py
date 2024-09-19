# -*- coding: utf-8 -*-
"""Abstract Mapper."""

# Standard Library Imports
import abc
import typing

__all__ = ["AbstractClassMapper"]


class AbstractClassMapper(abc.ABC):
    """Represents an abstract class mapper."""

    @property
    @abc.abstractmethod
    def cls(self) -> type:
        """Mapped class."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def schema(self) -> typing.Any:
        """Mapped schema."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def properties(self) -> typing.Dict[str, typing.Any]:
        """Mapped properties."""
        raise NotImplementedError
