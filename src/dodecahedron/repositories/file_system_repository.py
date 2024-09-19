# -*- coding: utf-8 -*-
"""File-System Repository."""

# Standard Library Imports
import typing

# Local Imports
from .abstract_repository import AbstractRepository
from ..wrappers import AbstractFileSystemWrapper

__all__ = ["AbstractFileSystemRepository"]


class AbstractFileSystemRepository(AbstractRepository):
    """Represents an abstract file-system repository.

    Args:
        __file: File.

    """

    def __init__(self, __file: typing.Any, /, *args, **kwargs) -> None:
        if not isinstance(__file, AbstractFileSystemWrapper):
            expected = "expected type 'AbstractFileSystemWrapper'"
            actual = f"got {type(__file)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(*args, **kwargs)
        self._file = __file
