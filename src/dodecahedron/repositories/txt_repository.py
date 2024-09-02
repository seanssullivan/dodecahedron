# -*- coding: utf-8 -*-
"""Txt Repository."""

# Standard Library Imports
import logging
import typing

# Local Imports
from .file_repository import AbstractFileRepository
from ..wrappers.txt_file_wrappers import AbstractTxtWrapper

__all__ = ["AbstractTxtRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractTxtRepository(AbstractFileRepository):
    """Represents an abstract `.txt` file repository.

    Args:
        __file: Text file.

    """

    def __init__(self, __file: typing.Any, /, *args, **kwargs) -> None:
        if not isinstance(__file, AbstractTxtWrapper):
            expected = "expected type 'AbstractTxtWrapper'"
            actual = f"got {type(__file)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(__file, *args, **kwargs)
