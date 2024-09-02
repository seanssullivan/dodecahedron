# -*- coding: utf-8 -*-
"""Abstract Wrapper."""

# Standard Library Imports
import abc
import logging
import os
import pathlib
import typing

# Local Imports
from .. import settings
from .. import utils

__all__ = [
    "AbstractFileSystemWrapper",
    "AbstractDirectoryWrapper",
    "AbstractFileWrapper",
]

# Initiate logger.
log = logging.getLogger("dodecahedron")

# Custom types
T = typing.TypeVar("T")


class AbstractFileSystemWrapper(abc.ABC):
    """Represents an abstract file-system wrapper."""

    def __init__(self, read_only: bool = False) -> None:
        self.read_only = read_only

    @property
    @abc.abstractmethod
    def extension(self) -> str:
        """File extension."""
        raise NotImplementedError

    @property
    def read_only(self) -> bool:
        """Whether read only."""
        return self._read_only

    @read_only.setter
    def read_only(self, value: bool) -> None:
        if not isinstance(value, bool):
            message = f"expected type 'bool', got {type(value)} instead"
            raise TypeError(message)

        self._read_only = value

    @abc.abstractmethod
    def open(self, *args, **kwargs) -> typing.IO:
        """Open file."""
        raise NotImplementedError

    def _open_file(self, filepath: os.PathLike, mode: str) -> typing.IO:
        """Open a file and return a file object.

        Args:
            filepath: Path to file.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        self._raise_for_mode(mode)
        result = open(filepath, mode=mode)
        return result

    def _raise_for_mode(self, mode: str) -> None:
        """Raise for invalid mode.

        Args:
            mode: Mode.

        Raises:
            ValueError: when mode is invalid.

        """
        if self.read_only and set(mode).intersection({"a", "w", "x"}):
            message = f"{mode!s} mode not allowed when read-only is 'True'"
            raise ValueError(message)


class AbstractDirectoryWrapper(AbstractFileSystemWrapper):
    """Represents an abstract wrapper class for directories.

    Args:
        directory: Directory which contains file(s).
        read_only (optional): Whether directory is read only. Default ``False``.

    Raises:
        TypeError: when `directory` is not type ``Path``.
        NotADirectoryError: when `directory` is not a valid directory.

    """

    def __init__(
        self,
        directory: os.PathLike,
        *,
        extension: typing.Optional[str] = None,
        read_only: bool = False,
    ) -> None:
        if not isinstance(directory, os.PathLike):
            expected = "expected type 'PathLike'"
            actual = f"got {type(directory)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if extension and not isinstance(extension, str):
            message = f"expected type 'str', got {type(extension)} instead"
            raise TypeError(message)

        if not os.path.exists(directory) or not os.path.isdir(directory):
            message = f"{directory!s} is not a valid directory"
            raise NotADirectoryError(message)

        super().__init__(read_only)
        self._directory = pathlib.Path(directory)
        self._extension = utils.standardize_file_extension(extension or "*")

    @property
    def directory(self) -> pathlib.Path:
        """Path to directory."""
        return self._directory

    @property
    def extension(self) -> str:
        """File extension."""
        return self._extension

    def __fspath__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.directory)

    def open(self, filename: str, /, mode: str = "r") -> typing.IO:
        """Open a file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        Raises:
            TypeError: when `encoding` is not type ``str``.

        """
        filepath = self._get_filepath(filename)
        result = self._open_file(filepath, mode)
        return result

    def _get_filepath(self, filename: str) -> pathlib.Path:
        """Get filepath.

        Args:
            filename: Filename.

        Returns:
            Filepath.

        """
        result = self._directory / filename
        if not result.exists():
            result = self.find(filename)

        utils.raise_for_extension(result, self.extension)
        return result

    def find(self, ref: str) -> pathlib.Path:
        """Find path for file in directory.

        Finds the filepath for a file in the source directory where the
        filename contains the provided substring.

        Args:
            ref: Substring for which to search.

        Returns:
            Path for file.

        Raises:
            FileNotFoundError: When no filenames match provided substring.

        """
        log.debug(
            "Searching for %(ref)s in %(dir)s",
            {"ref": ref, "dir": self._directory},
        )
        try:
            filename = utils.set_extension(ref, self.extension)
            filepath = next(path for path in self._directory.rglob(filename))

        except StopIteration as err:
            message = f"{self._directory / filename} not found"
            raise FileNotFoundError(message) from err

        else:
            log.debug("Found %s", filepath)
            return filepath


class AbstractFileWrapper(AbstractFileSystemWrapper):
    """Represents an abstract wrapper class for files.

    Args:
        filepath: Path to file.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        TypeError: when `filepath` is not type ``PathLike``.
        IsADirectoryError: when `filepath` points to a directory.

    """

    def __init__(
        self, filepath: os.PathLike, *, read_only: bool = False
    ) -> None:
        if not isinstance(filepath, os.PathLike):
            message = f"expected type 'PathLike', got {type(filepath)} instead"
            raise TypeError(message)

        if os.path.isdir(filepath):
            message = f"{filepath!s} is a directory"
            raise IsADirectoryError(message)

        super().__init__(read_only)
        self._filepath = pathlib.Path(filepath)

    @property
    def filepath(self) -> pathlib.Path:
        """Path to file."""
        return self._filepath

    @property
    def extension(self) -> str:
        """File extension."""
        return self._filepath.suffix

    def __fspath__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.filepath)

    def open(self, mode: str = "rb") -> typing.IO:
        """Open file and return a file object.

        Args:
            mode (optional): Mode. Default ``rb``.

        Returns:
            File object.

        """
        result = self._open_file(self._filepath, mode=mode)
        return result


class AbstractTextWrapper(AbstractFileSystemWrapper):
    """Represents an abstract wrapper class for text files.

    Args:
        *args: Positional arguments.
        encoding (optional): File encoding. Default `utf-8`.
        newline (optional): Newline character. Default ``None``.
        **kargs: Keyword arguments.

    Raises:
        TypeError: when `encoding` is not type ``str``.

    """

    def __init__(
        self,
        *args,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        newline: typing.Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(encoding, str):
            message = f"expected type 'str', got {type(encoding)} instead"
            raise TypeError(message)

        self._encoding = encoding
        self._newline = newline

    @property
    def encoding(self) -> str:
        """Expected file encoding."""
        return self._encoding

    @property
    def newline(self) -> typing.Optional[str]:
        """Newline character."""
        return self._newline

    def _open_file(self, filepath: os.PathLike, mode: str) -> typing.IO:
        """Open a file and return a file object.

        Args:
            filepath: Path to file.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        encoding = self._get_encoding_for_file_mode(mode)
        newline = self._get_newline_for_file_mode(mode)
        result = open(
            filepath,
            mode=mode,
            encoding=encoding,
            newline=newline,
        )
        return result

    def _get_encoding_for_file_mode(self, mode: str) -> typing.Optional[str]:
        """Get encoding for file mode.

        Args:
            mode: Mode.

        Returns:
            Encoding.

        """
        result = self._encoding if "b" not in mode else None
        return result

    def _get_newline_for_file_mode(self, mode: str) -> typing.Optional[str]:
        """Get newline for file mode.

        Args:
            mode: Mode.

        Returns:
            Newline.

        """
        result = self._newline if "b" not in mode else None
        return result


class AbstractIOWrapper(typing.IO):
    """Represents an abstract I/O wrapper class for files.

    Args:
        __file: File.

    """

    @property
    @abc.abstractmethod
    def file(self) -> typing.IO:
        """File."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def closed(self) -> bool:
        """Whether file is closed."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def read_only(self) -> bool:
        """Whether read only."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Close `.xlsx` file."""
        raise NotImplementedError
