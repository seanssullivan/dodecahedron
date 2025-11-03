# -*- coding: utf-8 -*-
"""Xlsx Repository."""

# Standard Library Imports
import logging
from typing import Any
from typing import Optional
from typing import Sequence

# Local Imports
from .file_system_repository import AbstractFileSystemRepository
from ..wrappers.xlsx_file_wrappers import AbstractXlsxWrapper

# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractXlsxRepository(AbstractFileSystemRepository):
    """Represents an abstract `.xlsx` file repository.

    Args:
        __file: Xlsx file.

    Attributes:
        columns: Columns names.

    """

    def __init__(self, __file: Any, /, *args: Any, **kwargs: Any) -> None:
        if not isinstance(__file, AbstractXlsxWrapper):
            expected = "expected type 'AbstractXlsxWrapper'"
            actual = f"got {type(__file)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(__file, *args, **kwargs)

    @property
    def columns(self) -> Optional[Sequence[Any]]:
        """Column names."""
        results = getattr(self._file, "fieldnames", None)
        return results
