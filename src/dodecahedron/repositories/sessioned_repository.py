# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from typing import Any
from types import MethodType

# Local Imports
from .abstract_repository import AbstractRepository

__all__ = ["SessionedRepository"]


class SessionedRepository(AbstractRepository):
    """Represents a sessioned repository.

    Attributes:
        session: Session.

    """

    @property
    @abc.abstractmethod
    def session(self) -> Any:
        """Session."""
        raise NotImplementedError

    def close(self, *args: Any, **kwargs: Any) -> Any:
        """Close connection to repository.

        Args:
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        result = self._call_method_on_session("close", *args, **kwargs)
        return result

    def commit(self, *args: Any, **kwargs: Any) -> Any:
        """Commit changes to repository.

        Args:
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        result = self._call_method_on_session("commit", *args, **kwargs)
        return result

    def rollback(self, *args: Any, **kwargs: Any) -> Any:
        """Rollback changes to repository.

        Args:
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        result = self._call_method_on_session("rollback", *args, **kwargs)
        return result

    def _call_method_on_session(
        self, __name: str, /, *args: Any, **kwargs: Any
    ) -> Any:
        """Call method on session.

        Args:
            __name: Name of method.
            *args (optional): Positional arguments.
            **kwargs (optional): Keyword arguments.

        """
        try:
            method: MethodType = getattr(self.session, __name)
            result = method(*args, **kwargs)

        except AttributeError:
            return None

        return result
