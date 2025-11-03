# -*- coding: utf-8 -*-
"""CSV Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import logging
from typing import Any
from typing import Optional
from typing import Sequence

# Local Imports
from .file_system_repository import AbstractFileSystemRepository
from ..wrappers.csv_file_wrappers import AbstractCsvWrapper

__all__ = ["AbstractCsvRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractCsvRepository(AbstractFileSystemRepository):
    """Represents an abstract `.csv` file repository.

    Args:
        __file: CSV file.

    Attributes:
        columns: Columns names.

    """

    def __init__(self, __file: Any, /, *args: Any, **kwargs: Any) -> None:
        if not isinstance(__file, AbstractCsvWrapper):
            expected = "expected type 'AbstractCsvWrapper'"
            actual = f"got {type(__file)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(__file, *args, **kwargs)

    @property
    def columns(self) -> Optional[Sequence[Any]]:
        """Column names."""
        results = getattr(self._file, "fieldnames", None)
        return results
