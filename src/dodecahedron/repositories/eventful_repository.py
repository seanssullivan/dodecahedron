# -*- coding: utf-8 -*-
"""Eventful Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from collections import deque
from typing import Deque
from typing import Generator
from typing import Iterable
from typing import List
from typing import Union

# Local Imports
from .abstract_repository import AbstractRepository
from ..messages import BaseEvent
from ..queue import MessageQueue

__all__ = ["EventfulRepository"]


class EventfulRepository(AbstractRepository):
    """Represents an eventful repository.

    Attributes:
        events: Events.

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._events = MessageQueue()

    @property
    def events(self) -> MessageQueue:
        """Events."""
        return self._events

    def collect_events(self) -> Generator[BaseEvent, None, None]:
        """Collect events.

        Yields:
            Events.

        """
        self._update_events()
        while self.events:
            yield self.events.popleft()

    def _update_events(self) -> None:
        """Update events."""
        events = self._get_child_events()
        self.events.extend(events)
        self.events.sort()

    def _get_child_events(self) -> List[BaseEvent]:
        """Get events from child objects.

        Returns:
            Events.

        """
        results = collect_events_from_objects(self.seen)
        return results


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def collect_events_from_objects(objs: Iterable) -> List[BaseEvent]:
    """Collect events from objects.

    Args:
        objs: Objects from which to collect events.

    Returns:
        Events.

    """
    results = []
    for obj in objs:
        events = collect_events_from_object(obj)
        results.extend(events)

    return results


def collect_events_from_object(obj: object) -> List[BaseEvent]:
    """Collect events from object.

    Args:
        obj: Object from which to collect events.

    Returns:
        Events.

    """
    events = get_events(obj)

    results = []
    while events:
        event = events.popleft()  # type: BaseEvent
        results.append(event)

    return results


def get_events(obj: object) -> Union[Deque[BaseEvent], MessageQueue]:
    """Get events from object.

    Args:
        obj: Object.

    Returns:
        Events.

    """
    result = getattr(obj, "events", MessageQueue())
    if not is_message_queue(result) and is_iterable(result):
        return MessageQueue(result)

    if not is_message_queue(result) and not is_iterable(result):
        expected = "expected type 'Deque' or 'MessageQueue'"
        actual = f"got {type(result)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)

    return result


# ----------------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------------
def is_iterable(obj: object) -> bool:
    """Check whether object is iterable.

    Args:
        obj: Object to check.

    Returns:
        Whether object is iterable.

    """
    result = hasattr(obj, "__iter__")
    return result


def is_message_queue(obj: object) -> bool:
    """Check whether object is a message queue.

    Args:
        obj: Object to check.

    Returns:
        Whether object is a queue.

    """
    result = isinstance(obj, (MessageQueue, deque))
    return result
