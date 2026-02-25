# -*- coding: utf-8 -*-
"""CSV File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import csv
import os
from typing import Any
from typing import Collection
from typing import Dict
from typing import IO
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

# Local Imports
from .abstract_file_wrappers import AbstractDirectoryWrapper
from .abstract_file_wrappers import AbstractFileWrapper
from .abstract_file_wrappers import AbstractTextWrapper
from .abstract_file_wrappers import AbstractIOWrapper
from ..utils import converters
from .. import errors
from .. import settings
from .. import utils

__all__ = [
    "AbstractCsvWrapper",
    "CsvDirectoryWrapper",
    "CsvFileWrapper",
    "CsvIOWrapper",
]


class AbstractCsvWrapper(AbstractTextWrapper):
    """Represents an abstract wrapper class for `.csv` files."""

    @property
    def delimiter(self) -> str:
        """Delimiter."""
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: Any) -> None:
        errors.raise_for_instance(value, str)
        self._delimiter: str = value

    @property
    def dialect(self) -> Union[csv.Dialect, str]:
        """Dialect."""
        return self._dialect

    @dialect.setter
    def dialect(self, value: Any) -> None:
        if not isinstance(value, (csv.Dialect, str)):
            expected = "expected type 'Dialect' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._dialect: Union[csv.Dialect, str] = value

    @property
    def fieldnames(self) -> Sequence[str]:
        """Fieldnames."""
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value: Any) -> None:
        errors.raise_for_instance(value, Sequence)
        self._fieldnames: Sequence[str] = value

    @property
    def quotechar(self) -> str:
        """Quote character."""
        return self._quotechar

    @quotechar.setter
    def quotechar(self, value: Any) -> None:
        errors.raise_for_instance(value, str)
        self._quotechar: str = value

    def _init_csv_io_wrapper(self, __file: IO[Any], /) -> CsvIOWrapper:
        """Initialize I/O wrapper for `.csv` file.

        Args:
            __file: File-like object.

        Returns:
            I/O wrapper instance.

        """
        result = CsvIOWrapper(__file)
        setattr(result, "_context", self)
        return result


class CsvDirectoryWrapper(AbstractCsvWrapper, AbstractDirectoryWrapper):
    """Implements a wrapper for `.csv` files in a directory.

    Args:
        directory: Directory from which to load `.csv` file(s).
        delimiter (optional): Delimiter. Default `,`.
        dialect (optional): Dialect. Default `excel`.
        encoding (optional): File encoding. Default `utf-8`.
        fieldnames (optional): Fieldnames. Default ``None``.
        newline (optional): Newline character. Default ``None``.
        quotechar (optional): Quote character. Default ``"``.
        read_only (optional): Whether file is read only. Default ``False``.

    """

    def __init__(
        self,
        directory: "os.PathLike[Any]",
        *,
        delimiter: str = settings.DEFAULT_CSV_DELIMITER,
        dialect: Union[csv.Dialect, str] = settings.DEFAULT_CSV_DIALECT,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        fieldnames: Optional[Sequence[str]] = None,
        newline: str = settings.DEFAULT_CSV_NEWLINE,
        quotechar: str = settings.DEFAULT_CSV_QUOTECHAR,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            directory,
            encoding=encoding,
            extension=settings.CSV_EXTENSION,
            newline=newline,
            read_only=read_only,
        )
        self.delimiter = delimiter
        self.dialect = dialect
        self.fieldnames = fieldnames or []
        self.quotechar = quotechar

    def open(self, filename: str, /, mode: str = "r") -> CsvIOWrapper:
        """Open a `.csv` file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        Raises:
            TypeError: when `encoding` is not type ``str``.

        """
        file = super().open(filename, mode=converters.to_text_file_mode(mode))
        result = self._init_csv_io_wrapper(file)
        return result


class CsvFileWrapper(AbstractCsvWrapper, AbstractFileWrapper):
    """Implements a wrapper for `.csv` files.

    Args:
        filepath: Path to `.csv` file.
        delimiter (optional): Delimiter. Default `,`.
        dialect (optional): Dialect. Default `excel`.
        encoding (optional): File encoding. Default `utf-8`.
        fieldnames (optional): Fieldnames. Default ``None``.
        newline (optional): Newline character. Default ``None``.
        quotechar (optional): Quote character. Default ``"``.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        ValueError: when `filepath` is not a `.csv` file.

    """

    def __init__(
        self,
        filepath: "os.PathLike[Any]",
        *,
        delimiter: str = settings.DEFAULT_CSV_DELIMITER,
        dialect: Union[csv.Dialect, str] = settings.DEFAULT_CSV_DIALECT,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        fieldnames: Optional[Sequence[str]] = None,
        newline: str = settings.DEFAULT_CSV_NEWLINE,
        quotechar: str = settings.DEFAULT_CSV_QUOTECHAR,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            filepath,
            encoding=encoding,
            newline=newline,
            read_only=read_only,
        )
        utils.raise_for_extension(filepath, settings.CSV_EXTENSION)

        self.delimiter = delimiter
        self.dialect = dialect
        self.fieldnames = fieldnames or []
        self.quotechar = quotechar

    def open(self, mode: str = "r") -> CsvIOWrapper:
        """Open the `.csv` file and return a file object.

        Args:
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        file = super().open(converters.to_text_file_mode(mode))
        result = self._init_csv_io_wrapper(file)
        return result


class CsvIOWrapper(AbstractIOWrapper):
    """Implements a I/O wrapper for `.csv` files."""

    def __init__(self, __file: IO[Any]) -> None:
        self._file = __file
        self._context: Optional[AbstractCsvWrapper] = None

    @property
    def file(self) -> IO[Any]:
        """File."""
        return self._file

    @property
    def closed(self) -> bool:
        """Whether file is closed."""
        return self._file.closed

    @property
    def context(self) -> Union[AbstractCsvWrapper, CsvIOWrapper]:
        """Context."""
        return self._context or self

    @property
    def delimiter(self) -> Optional[str]:
        """Delimiter."""
        result = getattr(self.context, "_delimiter", None)
        return result

    @delimiter.setter
    def delimiter(self, value: Any) -> None:
        errors.raise_for_instance(value, str)
        setattr(self.context, "_delimiter", value)

    @property
    def dialect(self) -> Optional[Union[csv.Dialect, str]]:
        """Dialect."""
        result = getattr(self.context, "_dialect", None)
        return result

    @dialect.setter
    def dialect(self, value: Any) -> None:
        if not isinstance(value, (csv.Dialect, str)):
            expected = "expected type 'Dialect' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        setattr(self.context, "_dialect", value)

    @property
    def fieldnames(self) -> Sequence[str]:
        """Fieldnames."""
        result = getattr(self.context, "_fieldnames", [])
        return result

    @fieldnames.setter
    def fieldnames(self, value: Any) -> None:
        errors.raise_for_instance(value, Sequence)
        setattr(self.context, "_fieldnames", value)

    @property
    def quotechar(self) -> Optional[str]:
        """Delimiter."""
        result = getattr(self.context, "_quotechar", None)
        return result

    @quotechar.setter
    def quotechar(self, value: Any) -> None:
        errors.raise_for_instance(value, str)
        setattr(self.context, "_quotechar", value)

    @property
    def read_only(self) -> bool:
        """Whether read only."""
        return getattr(self._context, "read_only")

    def __enter__(self) -> CsvIOWrapper:
        return self

    def __exit__(self, *_) -> None:
        self.close()
        return

    def close(self) -> None:
        """Close `.csv` file."""
        self._file.close()

    def read(self, n: int = -1, /) -> str:
        """Read content of `.csv` file.

        Returns:
            Content.

        """
        result = self._file.read(n)
        return result

    def readline(self, limit: int = -1, /) -> str:
        """Read line from `.csv` file.

        Returns:
            Line.

        """
        result = self._file.readline(limit)
        return result

    def readlines(self, hint: int = -1, /) -> List[Any]:
        """Read lines from `.csv` file.

        Returns:
            Lines.

        """
        result = self._file.readlines(hint)
        return result

    def read_record(self) -> Dict[str, Any]:
        """Read record from `.csv` file.

        Returns:
            Record.

        """
        reader = self._get_record_reader()
        result: Dict[str, Any] = reader.read_record()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return result

    def read_records(self) -> List[Dict[str, Any]]:
        """Read records from `.csv` file.

        Returns:
            Records.

        """
        reader = self._get_record_reader()
        results = reader.read_records()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return results

    def _get_record_reader(self) -> _CsvRecordReader:
        """Get record reader for `.csv` file..

        Returns:
            Reader.

        """
        if not hasattr(self, "_record_reader"):
            self._start_record_reader()

        result: _CsvRecordReader = getattr(self, "_record_reader")
        return result

    def _start_record_reader(self) -> None:
        """Start record reader for `.csv` file."""
        reader = _CsvRecordReader(self)
        setattr(self, "_record_reader", reader)

    def read_row(self) -> List[str]:
        """Read row from `.csv` file.

        Returns:
            Row.

        """
        reader = self._get_row_reader()
        result = reader.read_row()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return result

    def read_rows(self) -> List[List[str]]:
        """Read rows from `.csv` file.

        Returns:
            Rows.

        """
        reader = self._get_row_reader()
        results = reader.read_rows()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return results

    def _get_row_reader(self) -> _CsvRowReader:
        """Get row reaader for `.csv` file.

        Returns:
            Reader.

        """
        if not hasattr(self, "_row_reader"):
            self._start_row_reader()

        result: _CsvRowReader = getattr(self, "_row_reader")
        return result

    def _start_row_reader(self) -> None:
        """Start row rwader for `.csv` file."""
        reader = _CsvRowReader(self)
        setattr(self, "_row_reader", reader)

    def write(self, content: str, /) -> int:  # type: ignore
        """Write content to `.txt` file.

        Args:
            content: Content.

        """
        result = self._file.write(content)
        return result

    def writelines(self, lines: Iterable[str], /) -> None:  # type: ignore
        """Write lines to `.txt` file.

        Args:
            lines: Lines.

        """
        result = self._file.writelines(lines)
        return result

    def write_header(self) -> None:
        """Write header."""
        writer = self._get_record_writer()
        writer.write_header()

    def write_record(self, record: Dict[str, Any], /) -> None:
        """Write record to `.csv` file.

        Args:
            record: Record to write.

        """
        writer = self._get_record_writer()
        writer.write_record(record)

    def write_records(self, records: Iterable[Dict[str, Any]], /) -> None:
        """Write records to `.csv` file.

        Args:
            records: Records to write.

        """
        writer = self._get_record_writer()
        writer.write_records(records)

    def _get_record_writer(self) -> _CsvRecordWriter:
        """Get record writer for `.csv` file.

        Returns:
            Writer.

        """
        if not hasattr(self, "_record_writer"):
            self._start_record_writer()

        result: _CsvRecordWriter = getattr(self, "_record_writer")
        return result

    def _start_record_writer(self) -> None:
        """Start record writer for `.csv` file."""
        writer = _CsvRecordWriter(self)
        setattr(self, "_record_writer", writer)

    def write_row(self, row: Iterable[Any], /) -> None:
        """Write row to `.csv` file.

        Args:
            row: Row to write.

        """
        writer = self._get_row_writer()
        writer.write_row(row)

    def write_rows(self, rows: Iterable[Iterable[Any]], /) -> None:
        """Write rows to `.csv` file.

        Args:
            rows: Rows to write.

        """
        writer = self._get_row_writer()
        writer.write_rows(rows)

    def _get_row_writer(self) -> _CsvRowWriter:
        """Get row `.csv` writer.

        Returns:
            Writer.

        """
        if not hasattr(self, "_writer"):
            self._start_row_writer()

        result: _CsvRowWriter = getattr(self, "_writer")
        return result

    def _start_row_writer(self) -> None:
        """Start standard `.csv` writer."""
        writer = _CsvRowWriter(self)
        setattr(self, "_writer", writer)


class _CsvRecordReader(Iterator[Any]):
    """Implements a record reader for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper", /) -> None:
        self._reader = csv.DictReader(
            __wrapper.file,
            fieldnames=__wrapper.fieldnames or None,
            dialect=__wrapper.dialect or settings.DEFAULT_CSV_DIALECT,
            delimiter=__wrapper.delimiter or settings.DEFAULT_CSV_DELIMITER,
            quotechar=__wrapper.quotechar,
        )

    @property
    def fieldnames(self) -> Sequence[str]:
        """Fieldnames."""
        return self._reader.fieldnames or []

    @fieldnames.setter
    def fieldnames(self, fieldnames: Sequence[str]) -> None:
        self._reader.fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._reader.line_num

    def __next__(self) -> Dict[str, Any]:
        result = self.read_record()
        return result

    def read_record(self) -> Dict[str, Any]:
        """Read record from `.csv` file.

        Returns
            Record.

        """
        result = next(self._reader)
        return result

    def read_records(self) -> List[Dict[str, Any]]:
        """Read records from `.csv` file.

        Returns:
            Records.

        """
        results = list(self._reader)
        return results


class _CsvRecordWriter:
    """Implements a record writer for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper") -> None:
        self._writer = csv.DictWriter(
            __wrapper.file,
            fieldnames=__wrapper.fieldnames,
            dialect=__wrapper.dialect or settings.DEFAULT_CSV_DIALECT,
            delimiter=__wrapper.delimiter or settings.DEFAULT_CSV_DELIMITER,
            quotechar=__wrapper.quotechar,
        )
        self._row_num = 0

    @property
    def fieldnames(self) -> Collection[str]:
        """Fieldnames."""
        return self._writer.fieldnames

    @fieldnames.setter
    def fieldnames(self, fieldnames: Collection[str]) -> None:
        self._writer.fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._row_num

    def write_header(self) -> None:
        """Write header."""
        self._writer.writeheader()
        self._row_num += 1

    def write_record(self, __record: Dict[str, Any], /) -> None:
        """Write record to `.csv` file.

        Args:
            __record: Record to write.

        """
        self._writer.writerow(__record)
        self._row_num += 1

    def write_records(self, __records: Iterable[Dict[str, Any]], /) -> None:
        """Write records to `.csv` file.

        Args:
            __records: Records to write.

        """
        self._writer.writerows(__records)
        self._row_num += len(list(__records))


class _CsvRowReader(Iterator[Any]):
    """Implements a row reader for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper") -> None:
        self._reader = csv.reader(
            __wrapper.file,
            __wrapper.dialect or settings.DEFAULT_CSV_DIALECT,
            delimiter=__wrapper.delimiter or settings.DEFAULT_CSV_DELIMITER,
            quotechar=__wrapper.quotechar,
        )
        self._fieldnames = __wrapper.fieldnames

    @property
    def fieldnames(self) -> Sequence[str]:
        """Fieldnames."""
        return self._fieldnames or []

    @fieldnames.setter
    def fieldnames(self, fieldnames: Sequence[str]) -> None:
        self._fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._reader.line_num

    def __next__(self) -> List[str]:
        result = self.read_row()
        return result

    def read_row(self) -> List[str]:
        """Read row from `.csv` file.

        Returns
            Row.

        """
        if self.row_num == 0 and self.fieldnames:
            result = self._read_first_row()
            return result

        if self.row_num == 0 and not self.fieldnames:
            self._read_header()

        result = next(self._reader)
        return result

    def read_rows(self) -> List[List[str]]:
        """Read rows from `.csv` file.

        Returns:
            Rows.

        """
        if self.row_num == 0 and self.fieldnames:
            results = [self._read_first_row(), *list(self._reader)]
            return results

        if self.row_num == 0 and not self.fieldnames:
            self._read_header()

        results = list(self._reader)
        return results

    def _read_header(self) -> None:
        """Read header.

        Raises:
            RuntimeError: when `fieldnames` is not empty.
            RuntimeError: when not on first line of file.

        """
        if self.fieldnames:  # sanity check
            message = "'fieldnames' is not empty"
            raise RuntimeError(message)

        if self.row_num != 0:
            message = "reader is not on first line of file"
            raise RuntimeError(message)

        self.fieldnames = next(self._reader)

    def _read_first_row(self) -> List[str]:
        """Read first row.

        Args:
            reader: Reader.

        Raises:
            RuntimeError: when `reader` is not on first line of file.

        """
        if self.row_num != 0:
            message = "reader is not on first line of file"
            raise RuntimeError(message)

        first_row = next(self._reader)
        if not self._is_header(first_row):
            return first_row

        result = next(self._reader)
        return result

    def _is_header(self, row: Sequence[Any]) -> bool:
        """Check whether row is header.

        Args:
            row: Row.

        Returns:
            Whether row is header.

        Raises:
            RuntimeError: when `fieldnames` is empty.

        """
        if not self.fieldnames:  # sanity check
            message = "'fieldnames' is empty"
            raise RuntimeError(message)

        result = not set(self.fieldnames).difference(row)
        return result


class _CsvRowWriter:
    """Implements a row writer for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper") -> None:
        self._writer = csv.writer(
            __wrapper.file,
            __wrapper.dialect or settings.DEFAULT_CSV_DIALECT,
            delimiter=__wrapper.delimiter or settings.DEFAULT_CSV_DELIMITER,
            quotechar=__wrapper.quotechar,
        )
        self._fieldnames = __wrapper.fieldnames
        self._row_num = 0

    @property
    def fieldnames(self) -> Sequence[str]:
        """Fieldnames."""
        return self._fieldnames or []

    @fieldnames.setter
    def fieldnames(self, fieldnames: Sequence[str]) -> None:
        self._fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._row_num

    def write_header(self) -> None:
        """Write header."""
        self.write_row(self.fieldnames)

    def write_row(self, __row: Iterable[Any], /) -> None:
        """Write row to `.csv` file.

        Args:
            __row: Row to write.

        """
        self._writer.writerow(__row)
        self._row_num += 1

    def write_rows(self, __rows: Iterable[Iterable[Any]], /) -> None:
        """Write rows to `.csv` file.

        Args:
            __rows: Rows to write.

        """
        self._writer.writerows(__rows)
        self._row_num += len(list(__rows))
