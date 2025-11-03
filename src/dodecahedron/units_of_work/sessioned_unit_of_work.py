# -*- coding: utf-8 -*-
"""Sessioned Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

# Local Imports
from .abstract_unit_of_work import AbstractUnitOfWork


# Custom types
T = TypeVar("T")

# Private attributes
SESSION_ATTR = "_session"


class SessionedUnitOfWork(AbstractUnitOfWork):
    """Class implements a sessioned unit of work.

    Args:
        *args (optional): Positional arguments.
        session_factory (optional): Function for creating a session.
        **kwargs (optional): Keyword arguments.

    Attributes:
        session: Session.

    """

    def __init__(
        self,
        *args: Any,
        session_factory: Callable[..., T],
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._session_factory = session_factory

    @property
    def session(self) -> Optional[T]:  # type: ignore
        """Session."""
        return getattr(self, SESSION_ATTR, None)

    def __enter__(self) -> SessionedUnitOfWork:
        setattr(self, SESSION_ATTR, self._session_factory())
        super().__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        super().__exit__(*args)
        self.close()

    def close(self) -> None:
        """Close session."""
        method = getattr(self.session, "close", None)
        if method is not None:
            method()

    def commit(self) -> None:
        """Commit changes."""
        super().commit()  # type: ignore
        method = getattr(self.session, "commit", None)
        if method is not None:
            method()

    def rollback(self) -> None:
        """Rollback changes."""
        super().rollback()  # type: ignore

        method = getattr(self.session, "rollback", None)
        if method is not None:
            method()
