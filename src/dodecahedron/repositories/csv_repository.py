# -*- coding: utf-8 -*-
"""CSV Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import logging
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List
from typing import Optional
from typing import Sequence

# Local Imports
from .file_system_repository import AbstractFileSystemRepository
from ..wrappers.csv_file_wrappers import CsvFileWrapper
from ..mappers import ClassMapper

__all__ = ["AbstractCsvFileRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractCsvFileRepository(AbstractFileSystemRepository):
    """Represents an abstract `.csv` file repository.

    Args:
        wrapper: CSV file wrapper.
        *args (optional): Positional arguments.
        mapper (optional): Mapper. Default ``None``.
        **kwargs (optional): Keyword arguments.

    Attributes:
        columns: Columns names.

    """

    def __init__(
        self,
        wrapper: Any,
        /,
        *args: Any,
        mapper: Optional["ClassMapper[Any]"] = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(wrapper, CsvFileWrapper):
            expected = "expected type 'CsvFileWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if mapper and not isinstance(mapper, ClassMapper):  # type: ignore
            expected = "expected type 'ClassMapper'"
            actual = f"got {type(mapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(wrapper, *args, **kwargs)
        self._mapper = mapper

    @property
    def columns(self) -> Optional[Sequence[Any]]:
        """Column names."""
        results = getattr(self._wrapper, "fieldnames", None)
        return results

    @property
    def mapper(self) -> Optional["ClassMapper[Any]"]:
        """Mapper."""
        return self._mapper

    def _read_records(self) -> List[Dict[Hashable, Any]]:
        """Read records from file.

        Returns:
            Records.

        """
        with self._wrapper.open() as file:
            results = getattr(file, "read_records")()

        return results

    def _write_records(self, records: List[Dict[Hashable, Any]], /) -> None:
        """Write records to file.

        Args:
            records: Records.

        """
        with self._wrapper.open("w") as file:
            getattr(file, "write_header")()
            results = getattr(file, "write_records")(records)

        return results
