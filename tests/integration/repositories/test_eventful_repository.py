# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import List
from typing import Optional
from typing import Union

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.models import AbstractAggregate
from dodecahedron.repositories import EventfulRepository
from dodecahedron.queues import MessageQueue
from ... import factories


class ExampleModel(AbstractAggregate):
    """Example model for testing."""

    def __init__(self, ref: int) -> None:
        self._events = MessageQueue()
        self._reference = ref

    def __eq__(self, other: object) -> bool:
        result = (
            self.reference == other.reference
            if isinstance(other, ExampleModel)
            else False
        )
        return result

    def __hash__(self) -> int:
        return hash(self.reference)

    @property
    def reference(self) -> int:
        return self._reference

    @property
    def events(self) -> MessageQueue:
        return self._events

    def __contains__(self, _: object) -> bool:
        raise NotImplementedError

    def add(self, obj: object) -> None:
        raise NotImplementedError

    def get(self, ref: Union[int, str]) -> object:
        raise NotImplementedError

    def remove(self, obj: object) -> None:
        raise NotImplementedError


class ExampleRepository(EventfulRepository):
    """Example repository for testing."""

    def __init__(self, objects: Optional[List[Any]] = None) -> None:
        super().__init__()
        self._objects = set(objects or [])

    def __contains__(self, obj: object) -> bool:
        return obj in self._objects

    def add(self, obj: object) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, ref: Union[int, str]) -> object:
        """Get object."""
        raise NotImplementedError

    def list(self) -> List[Any]:
        """List objects."""
        raise NotImplementedError

    def remove(self, obj: object) -> None:
        """Remove object."""
        raise NotImplementedError

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""

    def close(self) -> None:
        """Close repository."""


def test_repository_has_message_queue() -> None:
    repo = ExampleRepository()
    assert isinstance(repo.events, MessageQueue)


def test_collects_events_from_child_objects() -> None:
    event1, event2, event3 = factories.make_events(3, delay=1e-6)

    repo = ExampleRepository()
    for idx, event in enumerate([event3, event2, event1]):
        model = ExampleModel(idx)
        model.events.append(event)
        repo.add(model)

    results = list(repo.collect_events())
    expected = [event1, event2, event3]
    assert results == expected
