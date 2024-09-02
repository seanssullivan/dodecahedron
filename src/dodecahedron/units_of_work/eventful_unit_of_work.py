# -*- coding: utf-8 -*-
"""Eventful Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
from typing import Generator

# Local Imports
from .abstract_unit_of_work import AbstractUnitOfWork
from ..messages import BaseEvent
from ..queue import MessageQueue

__all__ = ["EventfulUnitOfWork"]


class EventfulUnitOfWork(AbstractUnitOfWork):
    """Class implements an eventful unit of work."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._events = MessageQueue()

    def __enter__(self) -> EventfulUnitOfWork:
        self._events.clear()
        super().__enter__()
        return self

    @property
    def events(self) -> MessageQueue:
        """Event queue."""
        return self._events

    def collect_events(self) -> Generator[BaseEvent, None, None]:
        """Collect events.

        Yields:
            Event.

        """
        while self.events:
            yield self.events.popleft()
