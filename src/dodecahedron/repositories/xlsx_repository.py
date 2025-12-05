# -*- coding: utf-8 -*-
"""Xlsx Repository."""

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
from ..wrappers.xlsx_file_wrappers import XlsxFileWrapper
from ..mappers import ClassMapper

__all__ = ["AbstractXlsxFileRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractXlsxFileRepository(AbstractFileSystemRepository):
    """Represents an abstract `.xlsx` file repository.

    Args:
        wrapper: Xlsx file wrapper.
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
        if not isinstance(wrapper, XlsxFileWrapper):
            expected = "expected type 'XlsxFileWrapper'"
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
        with self._wrapper.open("wb") as file:
            getattr(file, "write_header")()
            results = getattr(file, "write_records")(records)

        return results
