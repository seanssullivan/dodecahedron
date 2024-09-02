# -*- coding: utf-8 -*-
"""TXT File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import logging
import io
import os
import typing

# Local Imports
from .abstract_file_wrappers import AbstractDirectoryWrapper
from .abstract_file_wrappers import AbstractFileWrapper
from .abstract_file_wrappers import AbstractTextWrapper
from ..utils import converters
from .. import settings
from .. import utils

__all__ = [
    "TxtDirectoryWrapper",
    "TxtFileWrapper",
]


# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractTxtWrapper(AbstractTextWrapper):
    """Represents an abstract wrapper class for `.txt` files."""

    def _init_txt_io_wrapper(
        self,
        __buffer: memoryview,
        /,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        newline: str = settings.DEFAULT_TXT_NEWLINE,
    ) -> TxtIOWrapper:
        """Initialize I/O wrapper for `.txt` file.

        Args:
            __buffer: Buffer.

        Returns:
            I/O wrapper instance.

        """
        result = TxtIOWrapper(
            __buffer,
            encoding=encoding,
            newline=newline,
        )
        setattr(result, "_context", self)
        return result


class TxtDirectoryWrapper(AbstractTxtWrapper, AbstractDirectoryWrapper):
    """Implements a wrapper for `.txt` files in a directory.

    Args:
        directory: Directory from which to load `.txt` file(s).
        encoding (optional): File encoding. Default `utf-8`.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        TypeError: when `directory` is not type ``Path``.
        TypeError: when `encoding` is not type ``str``.
        NotADirectoryError: when `directory` is not a valid directory.

    """

    def __init__(
        self,
        directory: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        newline: typing.Optional[str] = None,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            directory,
            encoding=encoding,
            extension=settings.TXT_EXTENSION,
            newline=newline,
            read_only=read_only,
        )

    def open(self, filename: str, /, mode: str = "r") -> TxtIOWrapper:
        """Open a `.txt` file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        Raises:
            TypeError: when `encoding` is not type ``str``.

        """

        file = super().open(filename, mode=converters.to_bytes_file_mode(mode))
        result = self._init_txt_io_wrapper(file)
        return result


class TxtFileWrapper(AbstractTxtWrapper, AbstractFileWrapper):
    """Implements a wrapper for `.txt` files.

    Args:
        filepath: Path to `.txt` file.
        encoding (optional): File encoding. Default `utf-8`.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        ValueError: when `filepath` is not a `.txt` file.

    """

    def __init__(
        self,
        filepath: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        newline: typing.Optional[str] = None,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            filepath,
            encoding=encoding,
            newline=newline,
            read_only=read_only,
        )
        utils.raise_for_extension(filepath, settings.TXT_EXTENSION)

    def open(self, mode: str = "r") -> TxtIOWrapper:
        """Open the `.txt` file and return a file object.

        Args:
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        file = super().open(converters.to_bytes_file_mode(mode))
        result = self._init_txt_io_wrapper(file)
        return result


class TxtIOWrapper(io.TextIOWrapper):
    """Implements a I/O wrapper for `.txt` files."""

    def __init__(
        self,
        buffer: memoryview,
        encoding: typing.Optional[str] = None,
        errors: typing.Optional[str] = None,
        newline: typing.Optional[str] = None,
        line_buffering: bool = False,
        write_through: bool = False,
    ) -> None:
        super().__init__(
            buffer,
            encoding=encoding,
            errors=errors,
            newline=newline,
            line_buffering=line_buffering,
            write_through=write_through,
        )
        self._context = None  # type: typing.Optional[AbstractTxtWrapper]

    def read(self) -> str:
        """Read content of `.txt` file.

        Returns:
            Content.

        """
        result = super().read()
        return result

    def readline(self) -> str:
        """Read line from `.txt` file.

        Returns:
            Line.

        """
        result = super().readline()
        return result

    def readlines(self) -> str:
        """Read lines from `.txt` file.

        Returns:
            Lines.

        """
        result = super().readlines()
        return result

    def write(self, content: str, /) -> None:
        """Write content to `.txt` file.

        Args:
            content: Content.

        """
        result = super().write(content)
        return result

    def writelines(self, lines: typing.Iterable[str], /) -> None:
        """Write lines to `.txt` file.

        Args:
            lines: Lines.

        """
        result = super().writelines(lines)
        return result
