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
from datetime import datetime
from typing import Any
from typing import Deque
from typing import Optional
from typing import Union
from typing import TYPE_CHECKING

# Local Imports
from .. import errors

if TYPE_CHECKING:
    from ..messages import AbstractMessage
    from ..queues import MessageQueue

__all__ = [
    "AbstractModel",
    "AbstractAggregate",
]


class AbstractModel(abc.ABC):
    """Class represents an abstract model.

    Models have one responsibility: to be unique. Therefore, subclasses must
    implement both the `__eq__` and `__hash__` methods.

    Args:
        created_at (optional): Datetime when object created. Default ``datetime.now()``.

    Attributes:
        parent: Parent model.
        created_at: Datetime when object created.
        is_removed: Whether object is removed.
        removed_at: Datetime when object removed.
        updated_at: Datetime when object updated.

    """

    def __init__(
        self,
        *,
        created_at: Optional[datetime] = None,
    ) -> None:
        # Context attributes
        self._context: Any = None

        # POArent attributes
        self._parent: Optional[AbstractAggregate] = None

        # Tracking attributes
        self._created_at = created_at or datetime.now()
        self._removed_at = None
        self._updated_at = None

    @abc.abstractmethod
    def __eq__(self, other: object, /) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    @property
    def context(self) -> Any:
        """Context."""
        return self._context

    @context.deleter
    def context(self) -> None:
        self._context = None

    @context.setter
    def context(self, obj: Any) -> None:
        self._context = obj

    @property
    def parent(self) -> Optional["AbstractAggregate"]:
        """Parent."""
        return self._parent

    @parent.setter
    def parent(self, obj: Any) -> None:
        errors.raise_for_instance(obj, AbstractAggregate)
        self._parent = obj

    @property
    def created_at(self) -> datetime:
        """When object was created."""
        return getattr(self, "_created_at")

    @property
    def is_removed(self) -> bool:
        """Whether object is removed."""
        return self.removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """Datetime when object was removed."""
        return getattr(self, "_removed_at", None)

    @removed_at.deleter
    def removed_at(self) -> None:
        setattr(self, "_removed_at", None)

    @removed_at.setter
    def removed_at(self, value: object) -> None:
        errors.raise_for_instance(value, datetime)
        setattr(self, "_removed_at", value)

    @property
    def updated_at(self) -> Optional[datetime]:
        """Datetime when object was updated."""
        return getattr(self, "_updated_at", None)

    @updated_at.deleter
    def updated_at(self) -> None:
        setattr(self, "_updated_at", None)

    @updated_at.setter
    def updated_at(self, value: object) -> None:
        errors.raise_for_instance(value, datetime)
        setattr(self, "_updated_at", value)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Update rate.

        Args:
            *args (optional): Positional arguments.
            **kwargs (optional): keyword arguments.

        """
        raise NotImplementedError


class AbstractAggregate(AbstractModel):
    """Class represents an abstract aggregate.

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
    def add(self, obj: object, /, *args: Any, **kwargs: Any) -> None:
        """Add object to aggregate.

        Args:
            obj: Object to add.
            *args (optional): Positional arguments.
            **kwargs (optional): keyword arguments.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: Any, /, *args: Any, **kwargs: Any) -> Optional[object]:
        """Get object in aggregate.

        Args:
            ref: Reference for object.
            *args (optional): Positional arguments.
            **kwargs (optional): keyword arguments.

        Returns:
            Object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: object, /, *args: Any, **kwargs: Any) -> None:
        """Remove object from aggregate.

        Args:
            obj: Object to remove.
            *args (optional): Positional arguments.
            **kwargs (optional): keyword arguments.

        """
        raise NotImplementedError
