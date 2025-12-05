# -*- coding: utf-8 -*-
"""Txt Repository."""

# Standard Library Imports
import logging
from typing import Any

# Local Imports
from .file_system_repository import AbstractFileSystemRepository
from ..wrappers.txt_file_wrappers import TxtFileWrapper

__all__ = ["AbstractTxtFileRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractTxtFileRepository(AbstractFileSystemRepository):
    """Represents an abstract `.txt` file repository.

    Args:
        wrapper: Text file wrapper.
        *args (optional): Positional arguments.
        **kwargs (optional): Keyword arguments.

    """

    def __init__(self, wrapper: Any, /, *args: Any, **kwargs: Any) -> None:
        if not isinstance(wrapper, TxtFileWrapper):
            expected = "expected type 'TxtFileWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(wrapper, *args, **kwargs)
