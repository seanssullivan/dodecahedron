# -*- coding: utf-8 -*-
"""Abstract Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
import abc
from collections import ChainMap
from typing import Any
from typing import MutableMapping
from typing import Optional
from typing import Type

__all__ = ["AbstractUnitOfWork"]


# Constants
AUTO_COMMIT_ATTR = "_auto_commit"


class AbstractUnitOfWork(abc.ABC):
    """Class represents an abstract unit of work."""

    def __init__(
        self,
        *,
        context: Optional[MutableMapping[str, Any]] = None,
    ) -> None:
        self._context = ChainMap(context or {}).new_child()

    @property
    def context(self) -> MutableMapping[str, Any]:
        """Context."""
        return self._context

    @property
    def auto_commit(self) -> bool:
        """Whether to auto commit.

        Raises:
            TypeError: when value is not type 'bool'.

        """
        result = getattr(self, AUTO_COMMIT_ATTR, False)
        return result

    @auto_commit.setter
    def auto_commit(self, value: bool) -> None:
        if not isinstance(value, bool):  # type: ignore
            message = f"expected type 'bool', got {type(value)} instead"
            raise TypeError(message)

        setattr(self, AUTO_COMMIT_ATTR, value)

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, exc: Optional[Type[Exception]], *_: Any) -> None:
        if self.auto_commit is True and not exc:
            self.commit()

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""
