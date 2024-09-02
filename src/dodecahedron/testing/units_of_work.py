# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations

# Third-Party Imports
from ..units_of_work import AbstractUnitOfWork
from ..units_of_work import EventfulUnitOfWork

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

    @property
    def rolled_back(self) -> bool:
        """Whether `rollback()` method was called."""
        result = getattr(self, ROLLED_BACK_ATTR, False)
        return result

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
