# -*- coding: utf-8 -*-
"""Queue.

This module defines base classes for queues.

"""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from __future__ import annotations
import abc
from collections import deque
from typing import Iterable
from typing import Iterator
from typing import Optional

# Local Imports
from .messages import BaseMessage
from .helpers import raise_for_instance

__all__ = ["MessageQueue"]


class AbstractQueue(abc.ABC):
    """Represents an abstract queue."""

    @abc.abstractmethod
    def __iter__(self) -> Iterator[object]:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def append(self, __obj: object, /) -> None:
        """Append object to queue.

        Args:
            __obj: Message to append to queue.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def extend(self, __iterable: Iterable[object], /) -> None:
        """Extend queue from iterable object.

        Args:
            __iterable: Iterable with which to extend queue.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def popleft(self) -> object:
        """Pop object from left side of queue."""
        raise NotImplementedError

    @abc.abstractmethod
    def sort(self) -> None:
        """Sort objects in queue."""
        raise NotImplementedError


class BaseQueue(AbstractQueue):
    """Implements a base class for queues.

    Args:
        __iterable (optional): Iterable of objects. Default ``None``.

    """

    def __new__(
        cls, __iterable: Optional[Iterable[object]] = None
    ) -> BaseQueue:
        if __iterable and not isinstance(__iterable, Iterable):
            raise TypeError("argument is not iterable")

        instance = super().__new__(cls)  # type: BaseQueue
        return instance

    def __init__(self, __iterable: Optional[Iterable[object]] = None) -> None:
        self._items = deque(__iterable or [])
        self.sort()

    def __iter__(self) -> Iterator[object]:
        return self

    def __len__(self) -> int:
        return len(self._items)

    def __next__(self) -> object:
        if len(self._items) == 0:
            raise StopIteration

        return self.popleft()

    def __repr__(self) -> str:
        return repr(list(self._items))

    def append(self, __item: object, /) -> None:
        """Append item to queue.

        Args:
            __item: Item to append to queue.

        """
        self._items.append(__item)
        self.sort()

    def extend(self, __iterable: Iterable[object], /) -> None:
        """Extend queue.

        Args:
            __iterable: Items with which to extend queue.

        """
        self._items.extend(__iterable)
        self.sort()

    def popleft(self) -> object:
        """Pop item from left side of queue."""
        return self._items.popleft()

    def sort(self) -> None:
        """Sort queue."""
        self._items = deque(sorted(self._items))

    def clear(self) -> None:
        """Clear queue."""
        self._items.clear()


class MessageQueue(BaseQueue):
    """Implements a message queue.

    Args:
        __iterable (optional): Iterable of messages. Default ``None``.

    """

    def __new__(
        cls, __iterable: Optional[Iterable[object]] = None
    ) -> MessageQueue:
        if __iterable is not None:
            for item in __iterable:
                raise_for_instance(item, BaseMessage)

        instance = super().__new__(cls)  # type: MessageQueue
        return instance

    def __iter__(self) -> Iterator[BaseMessage]:
        return self

    def __next__(self) -> BaseMessage:
        return super().__next__()

    def append(self, __item: object, /) -> None:
        """Append message to queue.

        Args:
            __item: Message to append to queue.

        """
        raise_for_instance(__item, BaseMessage)
        super().append(__item)

    def extend(self, __iterable: Iterable[object], /) -> None:
        """Extend queue with messages.

        Args:
            __iterable: Messages with which to extend queue.

        """
        messages = []
        for item in __iterable:
            raise_for_instance(item, BaseMessage)
            messages.append(item)

        super().extend(messages)

    def popleft(self) -> BaseMessage:
        """Pop message from left side of queue."""
        return super().popleft()
