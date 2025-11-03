# -*- coding: utf-8 -*-
"""Queues.

This module defines classes for queues.

"""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from __future__ import annotations
import abc
from collections import deque
from typing import Any
from typing import Deque
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

# Local Imports
from .messages import AbstractMessage
from .helpers import raise_for_instance

__all__ = [
    "AbstractQueue",
    "MessageQueue",
]


class AbstractQueue(abc.ABC):
    """Represents an abstract queue.

    Args:
        __iterable (optional): Iterable of objects. Default ``None``.

    """

    def __init__(
        self: Self,
        __iterable: Optional[Iterable[object]] = None,
    ) -> None:
        raise_for_iterable(__iterable)

        self._items: Deque[Any] = deque(__iterable or [])
        self.sort()

    def __iter__(self) -> Iterator[object]:
        return self

    def __len__(self) -> int:
        return len(self._items)

    def __next__(self) -> Any:
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


class MessageQueue(AbstractQueue):
    """Implements a message queue.

    Args:
        __iterable (optional): Iterable of messages. Default ``None``.

    """

    def __new__(
        cls: Type[Self],
        __iterable: Optional[Iterable[object]] = None,
    ) -> MessageQueue:
        if __iterable is not None:
            for item in __iterable:
                raise_for_instance(item, AbstractMessage)

        instance = super().__new__(cls)
        return instance

    def __iter__(self) -> Iterator[AbstractMessage]:
        return self

    def __next__(self) -> AbstractMessage:
        return super().__next__()

    def append(self, __item: object, /) -> None:
        """Append message to queue.

        Args:
            __item: Message to append to queue.

        """
        raise_for_instance(__item, AbstractMessage)
        super().append(__item)

    def extend(self, __iterable: Iterable[object], /) -> None:
        """Extend queue with messages.

        Args:
            __iterable: Messages with which to extend queue.

        """
        messages: List[AbstractMessage] = []
        for item in __iterable:
            raise_for_instance(item, AbstractMessage)
            messages.append(item)  # type: ignore

        super().extend(messages)

    def popleft(self) -> AbstractMessage:
        """Pop message from left side of queue."""
        return super().popleft()  # type: ignore


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def raise_for_iterable(__obj: object) -> None:
    """Raise error when object is not iterable.

    Args:
        __obj: Object to check.

    Raises:
        TypeError: when object is not iterable.

    """
    if __obj and not isinstance(__obj, Iterable):
        raise TypeError("argument is not iterable")
