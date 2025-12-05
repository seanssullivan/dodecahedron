# -*- coding: utf-8 -*-
"""File-System Repository."""

# Standard Library Imports
import pathlib
from typing import Any
from typing import Optional

# Local Imports
from .abstract_repository import AbstractRepository
from ..wrappers import AbstractFileSystemWrapper

__all__ = ["AbstractFileSystemRepository"]


class AbstractFileSystemRepository(AbstractRepository):
    """Represents an abstract file-system repository.

    Args:
        wrapper: File-system wrapper.
        *args (optional): Positional arguments.
        **kwargs (optional): Keyword arguments.

    """

    def __init__(self, wrapper: Any, /, *args: Any, **kwargs: Any) -> None:
        if not isinstance(wrapper, AbstractFileSystemWrapper):
            expected = "expected type 'AbstractFileSystemWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(*args, **kwargs)
        self._wrapper = wrapper

    @property
    def path(self) -> Optional[pathlib.Path]:
        """Path."""
        result = getattr(self._wrapper, "path", None)
        return result
