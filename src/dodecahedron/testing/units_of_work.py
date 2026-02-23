# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from typing import Any

# Third-Party Imports
from ..units_of_work import AbstractUnitOfWork
from ..units_of_work import EventfulUnitOfWork
from .. import helpers

__all__ = ["FakeUnitOfWork", "FakeEventfulUnitOfWork"]


# Private Attributes
COMMITTED_ATTR = "_committed"
ROLLED_BACK_ATTR = "_rolled_back"


class FakeUnitOfWork(AbstractUnitOfWork):
    """Implements a fake unit of work."""

    @property
    def committed(self) -> bool:
        """Whether `commit()` method was called."""
        result = getattr(self, COMMITTED_ATTR, False)
        return result

    @committed.setter
    def committed(self, value: Any) -> None:
        helpers.raise_for_instance(value, bool)
        setattr(self, COMMITTED_ATTR, value)

    @property
    def rolled_back(self) -> bool:
        """Whether `rollback()` method was called."""
        result = getattr(self, ROLLED_BACK_ATTR, False)
        return result

    @rolled_back.setter
    def rolled_back(self, value: Any) -> None:
        helpers.raise_for_instance(value, bool)
        setattr(self, ROLLED_BACK_ATTR, value)

    def __enter__(self) -> FakeUnitOfWork:
        return self

    def commit(self) -> None:
        """Commit changes."""
        setattr(self, COMMITTED_ATTR, True)

    def rollback(self) -> None:
        """Rollback changes."""
        setattr(self, ROLLED_BACK_ATTR, True)


class FakeEventfulUnitOfWork(FakeUnitOfWork, EventfulUnitOfWork):
    """Implements a fake eventful unit of work."""
