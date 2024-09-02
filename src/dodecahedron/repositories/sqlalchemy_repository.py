# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any

# Third-Party Imports
from sqlalchemy.orm import Session

# Local Imports
from .sessioned_repository import SessionedRepository

__all__ = ["AbstractSqlAlchemyRepository"]


class AbstractSqlAlchemyRepository(SessionedRepository):
    """Represents an abstract SQLAlchemy repository.

    The repository uses SQLAlchemy to read data from a database and to handle
    relevant CRUD operations.

    Attributes:
        session: SQLAlchemy session.

    .. _SQLAlchemy Documentation:
        https://docs.sqlalchemy.org/

    """

    def __init__(self, session: Session, /, *args, **kwargs) -> None:
        if not isinstance(session, Session):
            message = f"expected type 'Session', got {type(session)} instead"
            raise TypeError(message)

        super().__init__(*args, **kwargs)
        self._session = session

    @property
    def session(self) -> Session:
        """Session."""
        return self._session

    def execute(self, *args, **kwargs) -> Any:
        """Call the execute method directly on the SQLAlchemy session.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result.

        """
        result = self.session.execute(*args, **kwargs)
        return result
