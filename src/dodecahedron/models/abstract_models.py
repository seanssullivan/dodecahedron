# -*- coding: utf-8 -*-
"""Abstract models.

This module defines abstract base classes for domain models.

Implementation based on 'Architecture Patterns in Python' domain model pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# pylint: disable=too-few-public-methods

# Standard Library Imports
import abc
from typing import Deque
from typing import Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..messages import AbstractMessage
    from ..queues import MessageQueue

__all__ = [
    "AbstractModel",
    "AbstractAggregate",
]


class AbstractModel(abc.ABC):
    """Represents an abstract model.

    Models have one responsibility: to be unique. Therefore, subclasses must
    implement both the `__eq__` and `__hash__` methods.

    """

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError


class AbstractAggregate(AbstractModel):
    """Represents an abstract aggregate.

    The primary purpose of an aggregate is not simply to hold a collection of
    objects; instead, the purpose of an aggregate is to record events raised
    by the domain model. In addition, the aggregate encapsulates whatever
    business logic is involved when adding and removing objects.

    Attributes:
        events: Events raised by the domain model.

    """

    @property
    @abc.abstractmethod
    def events(self) -> Union[Deque["AbstractMessage"], "MessageQueue"]:
        """Events raised."""
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, obj: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, obj: object) -> None:
        """Add object to aggregate."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: str) -> object:
        """Get object in aggregate."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: object) -> None:
        """Remove object from aggregate."""
        raise NotImplementedError
