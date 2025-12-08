# -*- coding: utf-8 -*-
"""PDF File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import os
from typing import Any
from typing import IO
from typing import Optional

# Local Imports
from .abstract_file_wrappers import AbstractDirectoryWrapper
from .abstract_file_wrappers import AbstractFileSystemWrapper
from .abstract_file_wrappers import AbstractFileWrapper
from .abstract_file_wrappers import AbstractIOWrapper
from ..utils import converters
from .. import settings
from .. import utils

__all__ = ["PdfDirectoryWrapper", "PdfFileWrapper"]


class AbstractPdfWrapper(AbstractFileSystemWrapper):
    """Represents an abstract wrapper class for `.pdf` files."""

    def _init_pdf_io_wrapper(self, __file: IO[Any], /) -> PdfIOWrapper:
        """Initialize I/O wrapper for `.pdf` file.

        Args:
            __file: File-like object.

        Returns:
            I/O wrapper instance.

        """
        result = PdfIOWrapper(__file)
        setattr(result, "_context", self)
        return result


class PdfDirectoryWrapper(AbstractPdfWrapper, AbstractDirectoryWrapper):
    """Implements a wrapper for `.pdf` files in a directory.

    Args:
        directory: Directory from which to load `.pdf` file(s).
        read_only (optional): Whether file is read only. Default ``False``.

    """

    def __init__(
        self,
        directory: "os.PathLike[Any]",
        *,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            directory,
            extension=settings.PDF_EXTENSION,
            read_only=read_only,
        )

    def open(self, filename: str, /, mode: str = "rb") -> IO[Any]:
        """Open a `.pdf` file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``rb``.

        Returns:
            File object.

        """
        file = super().open(filename, mode=converters.to_bytes_file_mode(mode))
        result = self._init_pdf_io_wrapper(file)
        return result


class PdfFileWrapper(AbstractPdfWrapper, AbstractFileWrapper):
    """Implements a wrapper for `.pdf` files.

    Args:
        filepath: Path to `.pdf` file.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        ValueError: when `filepath` is not a `.pdf` file.

    """

    def __init__(
        self,
        filepath: "os.PathLike[Any]",
        *,
        read_only: bool = False,
    ) -> None:
        super().__init__(filepath, read_only=read_only)
        utils.raise_for_extension(filepath, settings.PDF_EXTENSION)

    def open(self, mode: str = "rb") -> IO[Any]:
        """Open the `.pdf` file and return a file object.

        Args:
            mode (optional): Mode. Default ``rb``.

        Returns:
            File object.

        """
        file = super().open(converters.to_bytes_file_mode(mode))
        result = self._init_pdf_io_wrapper(file)
        return result


class PdfIOWrapper(AbstractIOWrapper):
    """Implements a I/O wrapper for `.pdf` files."""

    def __init__(self, __file: IO[Any]) -> None:
        self._file = __file
        self._context: Optional[AbstractPdfWrapper] = None

    @property
    def file(self) -> IO[Any]:
        """File."""
        return self._file

    @property
    def closed(self) -> bool:
        """Check whether file is closed.

        Returns:
            Whether file is closed.

        """
        return self._file.closed

    def __enter__(self) -> PdfIOWrapper:
        return self

    def __exit__(self, *_) -> None:
        self.close()
        return

    def close(self) -> None:
        """Close `.pdf` file."""
        self._file.close()
