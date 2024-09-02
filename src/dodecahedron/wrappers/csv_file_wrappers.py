# -*- coding: utf-8 -*-
"""CSV File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import abc
import collections
import csv
import os
import typing

# Local Imports
from .abstract_file_wrappers import AbstractDirectoryWrapper
from .abstract_file_wrappers import AbstractFileWrapper
from .abstract_file_wrappers import AbstractTextWrapper
from .abstract_file_wrappers import AbstractIOWrapper
from ..utils import converters
from .. import settings
from .. import utils

__all__ = [
    "AbstractCsvWrapper",
    "CsvDirectoryWrapper",
    "CsvFileWrapper",
]


class AbstractCsvWrapper(AbstractTextWrapper):
    """Represents an abstract wrapper class for `.csv` files."""

    @property
    @abc.abstractmethod
    def delimiter(self) -> str:
        """Delimiter."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dialect(self) -> typing.Union[csv.Dialect, str]:
        """Dialect."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def quotechar(self) -> str:
        """Quote character."""
        raise NotImplementedError

    def _init_csv_io_wrapper(self, __file: typing.IO, /) -> CsvIOWrapper:
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
        directory: os.PathLike,
        *,
        delimiter: str = settings.DEFAULT_CSV_DELIMITER,
        dialect: typing.Union[csv.Dialect, str] = settings.DEFAULT_CSV_DIALECT,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        fieldnames: typing.Optional[typing.Sequence] = None,
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
        self._delimiter = delimiter
        self._dialect = dialect
        self._fieldnames = fieldnames
        self._quotechar = quotechar

    @property
    def delimiter(self) -> str:
        """Delimiter."""
        return self._delimiter

    @property
    def dialect(self) -> typing.Union[csv.Dialect, str]:
        """Dialect."""
        return self._dialect

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._fieldnames

    @property
    def quotechar(self) -> str:
        """Quote character."""
        return self._quotechar

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
        filepath: os.PathLike,
        *,
        delimiter: str = settings.DEFAULT_CSV_DELIMITER,
        dialect: typing.Union[csv.Dialect, str] = settings.DEFAULT_CSV_DIALECT,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        fieldnames: typing.Optional[typing.Sequence] = None,
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

        self._delimiter = delimiter
        self._dialect = dialect
        self._fieldnames = fieldnames
        self._quotechar = quotechar

    @property
    def delimiter(self) -> str:
        """Delimiter."""
        return self._delimiter

    @property
    def dialect(self) -> typing.Union[csv.Dialect, str]:
        """Dialect."""
        return self._dialect

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._fieldnames

    @property
    def quotechar(self) -> str:
        """Quote character."""
        return self._quotechar

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

    def __init__(self, __file: typing.IO) -> None:
        self._file = __file
        self._context = None  # type: typing.Optional[AbstractCsvWrapper]

    @property
    def file(self) -> typing.IO:
        """File."""
        return self._file

    @property
    def closed(self) -> bool:
        """Whether file is closed."""
        return self._file.closed

    @property
    def delimiter(self) -> typing.Optional[str]:
        """Delimiter."""
        default = getattr(self._context, "delimiter", None)
        result = getattr(self, "_delimiter", default)
        return result

    @delimiter.setter
    def delimiter(self, value: typing.Any) -> None:
        if not isinstance(value, str):
            message = f"expected type 'str', got {type(value)} instead"
            raise TypeError(message)

        setattr(self, "_delimiter", value)

    @property
    def dialect(self) -> typing.Optional[typing.Union[csv.Dialect, str]]:
        """Dialect."""
        default = getattr(self._context, "dialect", None)
        result = getattr(self, "_dialect", default)
        return result

    @dialect.setter
    def dialect(self, value: typing.Any) -> None:
        if not isinstance(value, (csv.Dialect, str)):
            expected = "expected type 'Dialect' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        setattr(self, "_dialect", value)

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        default = getattr(self._context, "fieldnames", None)
        result = getattr(self, "_fieldnames", default)
        return result

    @fieldnames.setter
    def fieldnames(self, value: typing.Any) -> None:
        if not isinstance(value, typing.Sequence):
            message = f"expected type 'Sequence', got {type(value)} instead"
            raise TypeError(message)

        setattr(self, "_fieldnames", value)

    @property
    def quotechar(self) -> typing.Optional[str]:
        """Delimiter."""
        default = getattr(self._context, "quotechar", None)
        result = getattr(self, "_quotechar", default)
        return result

    @quotechar.setter
    def quotechar(self, value: typing.Any) -> None:
        if not isinstance(value, str):
            message = f"expected type 'str', got {type(value)} instead"
            raise TypeError(message)

        setattr(self, "_quotechar", value)

    @property
    def read_only(self) -> bool:
        """Whether read only."""
        return getattr(self._context, "read_only")  # type: bool

    def __enter__(self) -> CsvIOWrapper:
        return self

    def __exit__(self, *_) -> None:
        self.close()
        return

    def close(self) -> None:
        """Close `.csv` file."""
        self._file.close()

    def read(self, size: typing.Optional[int] = None, /) -> str:
        """Read content of `.csv` file.

        Returns:
            Content.

        """
        result = self._file.read(size)
        return result

    def readline(self, size: int = -1, /) -> str:
        """Read line from `.csv` file.

        Returns:
            Line.

        """
        result = self._file.readline(size)
        return result

    def readlines(self, hint: int = -1, /) -> str:
        """Read lines from `.csv` file.

        Returns:
            Lines.

        """
        result = self._file.readlines(hint)
        return result

    def read_record(self) -> dict:
        """Read record from `.csv` file.

        Returns:
            Record.

        """
        reader = self._get_record_reader()
        result = reader.read_record()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return result

    def read_records(self) -> typing.List[dict]:
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

        result = getattr(self, "_record_reader")  # type: _CsvRecordReader
        return result

    def _start_record_reader(self) -> None:
        """Start record reader for `.csv` file."""
        reader = _CsvRecordReader(self)
        setattr(self, "_record_reader", reader)

    def read_row(self) -> list:
        """Read row from `.csv` file.

        Returns:
            Row.

        """
        reader = self._get_row_reader()
        result = reader.read_row()

        if not self.fieldnames:
            self.fieldnames = reader.fieldnames

        return result

    def read_rows(self) -> typing.List[list]:
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

        result = getattr(self, "_row_reader")  # type: _CsvRowReader
        return result

    def _start_row_reader(self) -> None:
        """Start row rwader for `.csv` file."""
        reader = _CsvRowReader(self)
        setattr(self, "_row_reader", reader)

    def write(self, content: str, /) -> None:
        """Write content to `.txt` file.

        Args:
            content: Content.

        """
        result = self._file.write(content)
        return result

    def writelines(self, lines: typing.Iterable[str], /) -> None:
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

    def write_record(self, record: dict, /) -> None:
        """Write record to `.csv` file.

        Args:
            record: Record to write.

        """
        writer = self._get_record_writer()
        writer.write_record(record)

    def write_records(self, records: typing.Iterable[dict], /) -> None:
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

        result = getattr(self, "_record_writer")  # type: _CsvRecordWriter
        return result

    def _start_record_writer(self) -> None:
        """Start record writer for `.csv` file."""
        writer = _CsvRecordWriter(self)
        setattr(self, "_record_writer", writer)

    def write_row(self, row: typing.Iterable, /) -> None:
        """Write row to `.csv` file.

        Args:
            row: Row to write.

        """
        writer = self._get_row_writer()
        writer.write_row(row)

    def write_rows(self, rows: typing.Iterable[typing.Iterable], /) -> None:
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

        result = getattr(self, "_writer")  # type: _CsvRowWriter
        return result

    def _start_row_writer(self) -> None:
        """Start standard `.csv` writer."""
        writer = _CsvRowWriter(self)
        setattr(self, "_writer", writer)


class _CsvRecordReader(collections.abc.Iterator):
    """Implements a record reader for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper", /) -> None:
        self._reader = csv.DictReader(
            __wrapper.file,
            fieldnames=__wrapper.fieldnames,
            dialect=__wrapper.dialect,
            delimiter=__wrapper.delimiter,
            quotechar=__wrapper.quotechar,
        )

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._reader.fieldnames

    @fieldnames.setter
    def fieldnames(self, fieldnames: typing.Sequence) -> None:
        self._reader.fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._reader.line_num

    def __next__(self) -> typing.List[dict]:
        result = self.read_record()
        return result

    def read_record(self) -> None:
        """Read record from `.csv` file.

        Returns
            Record.

        """
        result = next(self._reader)
        return result

    def read_records(self) -> typing.List[typing.List[str]]:
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
            dialect=__wrapper.dialect,
            delimiter=__wrapper.delimiter,
            quotechar=__wrapper.quotechar,
        )
        self._row_num = 0

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._writer.fieldnames

    @fieldnames.setter
    def fieldnames(self, fieldnames: typing.Sequence) -> None:
        self._writer.fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._row_num

    def write_header(self) -> None:
        """Write header."""
        self._writer.writeheader()
        self._row_num += 1

    def write_record(self, __record: dict, /) -> None:
        """Write record to `.csv` file.

        Args:
            __record: Record to write.

        """
        self._writer.writerow(__record)
        self._row_num += 1

    def write_records(self, __records: typing.Iterable[dict], /) -> None:
        """Write records to `.csv` file.

        Args:
            __records: Records to write.

        """
        self._writer.writerows(__records)
        self._row_num += len(__records)


class _CsvRowReader(collections.abc.Iterator):
    """Implements a row reader for `.csv` files."""

    def __init__(self, __wrapper: "CsvIOWrapper") -> None:
        self._reader = csv.reader(
            __wrapper.file,
            __wrapper.dialect,
            delimiter=__wrapper.delimiter,
            quotechar=__wrapper.quotechar,
        )
        self._fieldnames = __wrapper.fieldnames

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, fieldnames: typing.Sequence) -> None:
        self._fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._reader.line_num

    def __next__(self) -> typing.List[str]:
        result = self.read_row()
        return result

    def read_row(self) -> None:
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

    def read_rows(self) -> typing.List[typing.List[str]]:
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

    def _read_first_row(self) -> typing.List[str]:
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

    def _is_header(self, row: typing.Sequence) -> bool:
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
            __wrapper.dialect,
            delimiter=__wrapper.delimiter,
            quotechar=__wrapper.quotechar,
        )
        self._fieldnames = __wrapper.fieldnames
        self._row_num = 0

    @property
    def fieldnames(self) -> typing.Optional[typing.Sequence]:
        """Fieldnames."""
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, fieldnames: typing.Sequence) -> None:
        self._fieldnames = fieldnames

    @property
    def row_num(self) -> int:
        """Row number."""
        return self._row_num

    def write_header(self) -> None:
        """Write header."""
        self.write_row(self.fieldnames)

    def write_row(self, __row: typing.Iterable, /) -> None:
        """Write row to `.csv` file.

        Args:
            __row: Row to write.

        """
        self._writer.writerow(__row)
        self._row_num += 1

    def write_rows(self, __rows: typing.Iterable[typing.Iterable], /) -> None:
        """Write rows to `.csv` file.

        Args:
            __rows: Rows to write.

        """
        self._writer.writerows(__rows)
        self._row_num += len(__rows)
