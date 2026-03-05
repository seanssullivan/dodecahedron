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
from ..wrappers.xlsx_file_wrappers import AbstractXlsxWrapper
from ..wrappers.xlsx_file_wrappers import XlsxDirectoryWrapper
from ..wrappers.xlsx_file_wrappers import XlsxFileWrapper
from ..mappers import AbstractMapper

__all__ = ["AbstractXlsxFileRepository"]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractXlsxRepository(AbstractFileSystemRepository):
    """Represents an abstract `.xlsx` repository.

    Args:
        wrapper: Xlsx wrapper.
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
        mapper: Optional[AbstractMapper] = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(wrapper, AbstractXlsxWrapper):
            expected = "expected type 'AbstractXlsxWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if mapper and not isinstance(mapper, AbstractMapper):  # type: ignore
            expected = "expected type 'AbstractMapper'"
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
    def mapper(self) -> Optional[AbstractMapper]:
        """Mapper."""
        return self._mapper


class AbstractXlsxDirectoryRepository(AbstractXlsxRepository):
    """Represents an abstract `.xlsx` directory repository.

    Args:
        wrapper: Xlsx directory wrapper.
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
        mapper: Optional[AbstractMapper] = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(wrapper, XlsxDirectoryWrapper):
            expected = "expected type 'XlsxDirectoryWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(wrapper, *args, mapper=mapper, **kwargs)

    def _read_records(self, filename: str, /) -> List[Dict[Hashable, Any]]:
        """Read records from file.

        Args:
            filename: Filename.

        Returns:
            Records.

        """
        with self._wrapper.open(filename) as file:
            results = getattr(file, "read_records")()

        return results

    def _write_records(
        self,
        filename: str,
        records: List[Dict[Hashable, Any]],
        /,
    ) -> None:
        """Write records to file.

        Args:
            filename: Filename.
            records: Records.

        """
        with self._wrapper.open(filename, mode="wb") as file:
            getattr(file, "write_header")()
            results = getattr(file, "write_records")(records)

        return results


class AbstractXlsxFileRepository(AbstractXlsxRepository):
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
        mapper: Optional[AbstractMapper] = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(wrapper, XlsxFileWrapper):
            expected = "expected type 'XlsxFileWrapper'"
            actual = f"got {type(wrapper)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(wrapper, *args, mapper=mapper, **kwargs)

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
