# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import List
from typing import Optional
from typing import Set

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.metaclasses import TrackerMeta
from dodecahedron.metaclasses.tracker import SEEN_ATTR


class SampleTracker(metaclass=TrackerMeta):
    def __init__(self, objs: Optional[List[Any]] = None) -> None:
        self._objects = set(objs or [])

    @property
    def seen(self) -> Set[Any]:
        return getattr(self, SEEN_ATTR, set())

    def add(self, obj: Any) -> None:
        self._objects.add(obj)

    def get(self, ref: str) -> Any:
        try:
            result = next(obj for obj in self._objects if obj == ref)
        except StopIteration:
            return None
        else:
            return result

    def list(self) -> List[Any]:
        return list(self._objects)

    def remove(self, obj: Any) -> None:
        self._objects.discard(obj)


def test_includes_added_object_in_seen_attribute() -> None:
    tracker = SampleTracker()
    tracker.add("success")
    assert "success" in tracker.seen


def test_includes_returned_object_in_seen_attribute() -> None:
    tracker = SampleTracker(["success"])
    tracker.get("success")
    assert "success" in tracker.seen


def test_includes_listed_objects_in_seen_attribute() -> None:
    tracker = SampleTracker(["one", "two", "three"])
    tracker.list()
    assert all([item in tracker.seen for item in ["one", "two", "three"]])


def test_includes_removed_object_in_seen_attribute() -> None:
    tracker = SampleTracker(["success"])
    tracker.remove("success")
    assert "success" in tracker.seen
