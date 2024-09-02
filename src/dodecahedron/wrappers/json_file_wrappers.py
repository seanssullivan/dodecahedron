# -*- coding: utf-8 -*-
"""JSON File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import abc
import json
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

__all__ = ["JsonDirectoryWrapper", "JsonFileWrapper"]


class AbstractJsonWrapper(AbstractTextWrapper):
    """Represents an abstract wrapper class for `.json` files."""

    @property
    @abc.abstractmethod
    def indent(self) -> typing.Optional[typing.Union[int, str]]:
        """Indent."""
        raise NotImplementedError

    def _init_json_io_wrapper(self, __file: typing.IO, /) -> JsonIOWrapper:
        """Initialize I/O wrapper for `.json` file.

        Args:
            __file: File-like object.

        Returns:
            I/O wrapper instance.

        """
        result = JsonIOWrapper(__file)
        setattr(result, "_context", self)
        return result


class JsonDirectoryWrapper(AbstractJsonWrapper, AbstractDirectoryWrapper):
    """Implements a wrapper for `.json` files in a directory.

    Args:
        directory: Directory from which to load `.json` file(s).
        encoding (optional): File encoding. Default `utf-8`.
        indent (optional): Indent. Default ``None``.
        read_only (optional): Whether file is read only. Default ``False``.

    """

    def __init__(
        self,
        directory: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        indent: typing.Optional[typing.Union[int, str]] = None,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            directory,
            encoding=encoding,
            extension=settings.JSON_EXTENSION,
            read_only=read_only,
        )
        self._indent = indent

    @property
    def indent(self) -> typing.Optional[typing.Union[int, str]]:
        """Indent."""
        return self._indent

    def open(self, filename: str, /, mode: str = "r") -> JsonIOWrapper:
        """Open a `.json` file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        Raises:
            TypeError: when `encoding` is not type ``str``.

        """

        file = super().open(filename, mode=converters.to_text_file_mode(mode))
        result = self._init_json_io_wrapper(file)
        return result


class JsonFileWrapper(AbstractJsonWrapper, AbstractFileWrapper):
    """Implements a wrapper for `.json` files.

    Args:
        filepath: Path to `.json` file.
        encoding (optional): File encoding. Default `utf-8`.
        indent (optional): Indent. Default ``None``.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        ValueError: when `filepath` is not a `.json` file.

    """

    def __init__(
        self,
        filepath: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        indent: typing.Optional[typing.Union[int, str]] = None,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            filepath,
            encoding=encoding,
            read_only=read_only,
        )
        utils.raise_for_extension(filepath, settings.JSON_EXTENSION)

        self._indent = indent

    @property
    def indent(self) -> typing.Optional[typing.Union[int, str]]:
        """Indent."""
        return self._indent

    def open(self, mode: str = "r") -> JsonIOWrapper:
        """Open the `.json` file and return a file object.

        Args:
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        file = super().open(converters.to_text_file_mode(mode))
        result = self._init_json_io_wrapper(file)
        return result


class JsonIOWrapper(AbstractIOWrapper):
    """Implements a I/O wrapper for `.json` files."""

    def __init__(self, __file: typing.IO) -> None:
        self._file = __file
        self._context = None  # type: typing.Optional[AbstractJsonWrapper]

    @property
    def file(self) -> typing.IO:
        """File."""
        return self._file

    @property
    def closed(self) -> bool:
        """Whether file is closed."""
        return self._file.closed

    @property
    def indent(self) -> typing.Optional[typing.Union[int, str]]:
        """Indent."""
        default = getattr(self._context, "indent", None)
        result = getattr(self, "_indent", default)
        return result

    @indent.setter
    def indent(self, value: typing.Any) -> None:
        if not isinstance(value, (int, str)):
            expected = "expected type 'int' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        setattr(self, "_indent", value)

    @property
    def read_only(self) -> bool:
        """Whether read only."""
        return getattr(self._context, "read_only")  # type: bool

    def __enter__(self) -> JsonIOWrapper:
        return self

    def __exit__(self, *_) -> None:
        self.close()
        return

    def close(self) -> None:
        """Close `.csv` file."""
        self._file.close()

    def dump(self, obj: typing.Any) -> None:
        """Serialize `obj` to file."""
        json.dump(obj, self._file)

    def load(self) -> typing.Any:
        """Deserialize contents of file."""
        result = json.load(self._file)
        return result
