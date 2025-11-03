# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from typing import List
from typing import Optional
from typing import Set
from typing import Union

# Third-Party Imports
from ..models import AbstractModel
from ..repositories import AbstractRepository
from ..repositories import EventfulRepository

__all__ = ["FakeRepository", "FakeEventfulRepository"]


# Constants
DEFAULT_KEY = "reference"

# Private Attributes
CLOSED_ATTR = "_closed"
COMMITTED_ATTR = "_committed"
ROLLED_BACK_ATTR = "_rolled_back"


class FakeRepository(AbstractRepository):
    """Implements a fake repository."""

    def __init__(
        self,
        objects: Optional[List[AbstractModel]] = None,
        key: str = DEFAULT_KEY,
    ) -> None:
        super().__init__()
        self._objects: Set[AbstractModel] = set(objects or [])
        self._key = key

    @property
    def closed(self) -> bool:
        """Whether `close()` method was called."""
        result = getattr(self, CLOSED_ATTR, False)
        return result

    @property
    def committed(self) -> bool:
        """Whether `commit()` method was called."""
        result = getattr(self, COMMITTED_ATTR, False)
        return result

    @property
    def rolled_back(self) -> bool:
        """Whether `rollback()` method was called."""
        result = getattr(self, ROLLED_BACK_ATTR, False)
        return result

    def __contains__(self, obj: AbstractModel) -> bool:
        return obj in self._objects

    def add(self, obj: AbstractModel) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, ref: Union[int, str]) -> Optional[AbstractModel]:
        """Get object.

        Args:
            ref: Reference to object.

        """
        results = (
            obj
            for obj in self._objects
            if getattr(obj, self._key, None) == ref
        )
        return next(results, None)

    def list(self) -> List[AbstractModel]:
        """List objects."""
        return list(self._objects)

    def remove(self, obj: AbstractModel) -> None:
        """Remove object."""
        self._objects.discard(obj)

    def commit(self) -> None:
        """Commit changes."""
        setattr(self, COMMITTED_ATTR, True)

    def rollback(self) -> None:
        """Rollback changes."""
        setattr(self, ROLLED_BACK_ATTR, True)

    def close(self) -> None:
        """Close repository."""
        setattr(self, CLOSED_ATTR, True)


class FakeEventfulRepository(FakeRepository, EventfulRepository):
    """Implements a fake eventful repository."""
