# -*- coding: utf-8 -*-
"""File Extension Utility Functions."""

# Standard Library Imports
import pathlib
from typing import TypeVar
from typing import Union

__all__ = [
    "has_extension",
    "raise_for_extension",
    "set_extension",
    "standardize_file_extension",
]


# Custom types
T = TypeVar("T")


def raise_for_extension(
    __file: Union[pathlib.Path, str], /, extension: str
) -> None:
    """Raise for incorrect file extension.

    Args:
        __file: Filename or filepath.
        extension: Expected file extension.

    Raises:
        ValueError: when filepath does not have expected extension.

    """
    if not has_extension(__file, extension):
        filename = pathlib.Path(__file).name
        message = f"{filename!s} is not a '{extension!s}' file"
        raise ValueError(message)


def has_extension(__file: Union[pathlib.Path, str], /, extension: str) -> bool:
    """Check whether file has expected extension.

    Args:
        __file: Filename or filepath.
        extension: Expected file extension.

    Returns:
        Whether file has expected extension.

    Raises:
        TypeError: when `filepath` is not type `Path` or `str`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(__file, (pathlib.Path, str)):
        message = f"expected type 'Path' or 'str', got {type(__file)} instead"
        raise TypeError(message)

    if isinstance(__file, pathlib.Path):
        return filepath_has_extension(__file, extension)

    if isinstance(__file, str):
        return filename_has_extension(__file, extension)


def filename_has_extension(__filename: str, /, extension: str) -> bool:
    """Check whether filename has expected extension.

    Args:
        __filename: Name of file.
        extension: Expected file extension.

    Returns:
        Whether file has expected extension.

    Raises:
        TypeError: when `filename` is not type `str`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(__filename, str):
        message = f"expected type 'str', got {type(__filename)} instead"
        raise TypeError(message)

    if not isinstance(extension, str):
        message = f"expected type 'str', got {type(extension)} instead"
        raise TypeError(message)

    expected = standardize_file_extension(extension)
    result = expected == "*" or __filename.endswith(f".{expected}")
    return result


def filepath_has_extension(
    __filepath: pathlib.Path, /, extension: str
) -> bool:
    """Check whether filepath has expected extension.

    Args:
        __filepath: Path to file.
        extension: Expected file extension.

    Returns:
        Whether file has expected extension.

    Raises:
        TypeError: when `filepath` is not type `Path`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(__filepath, pathlib.Path):
        message = f"expected type 'Path', got {type(__filepath)} instead"
        raise TypeError(message)

    if not isinstance(extension, str):
        message = f"expected type 'str', got {type(extension)} instead"
        raise TypeError(message)

    actual = standardize_file_extension(__filepath.suffix)
    expected = standardize_file_extension(extension)
    result = expected == "*" or actual == expected
    return result


def set_extension(__file: T, extension: str) -> T:
    """Set extension on file.

    Args:
        __file: Filename or filepath.
        extension: File extension.

    Returns:
        File with extension.

    Raises:
        TypeError: when `filename` is not type `Path` or `str`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(__file, (pathlib.Path, str)):
        message = f"expected type 'Path' or 'str', got {type(__file)} instead"
        raise TypeError(message)

    if isinstance(__file, pathlib.Path):
        return set_extension_on_filepath(__file, extension)

    if isinstance(__file, str):
        return set_extension_on_filename(__file, extension)


def set_extension_on_filename(filename: str, extension: str) -> str:
    """Set extension on filename.

    Args:
        filename: Name of file.
        extension: File extension.

    Returns:
        Filename with extension.

    Raises:
        TypeError: when `filename` is not type `str`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(filename, str):
        message = f"expected type 'str', got {type(filename)} instead"
        raise TypeError(message)

    if not isinstance(extension, str):
        message = f"expected type 'str', got {type(extension)} instead"
        raise TypeError(message)

    standardized_extension = standardize_file_extension(extension)
    result = (
        f"*{filename!s}*.{standardized_extension!s}"
        if not filename.endswith(f".{standardized_extension!s}")
        else f"*{filename!s}"
    )
    return result


def set_extension_on_filepath(
    filepath: pathlib.Path, extension: str
) -> pathlib.Path:
    """Set extension on filepath.

    Args:
        filepath: Path to file.
        extension: File extension.

    Returns:
        Filepath with extension.

    Raises:
        TypeError: when `filepath` is not type `Path`.
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(filepath, pathlib.Path):
        message = f"expected type 'Path', got {type(filepath)} instead"
        raise TypeError(message)

    if not isinstance(extension, str):
        message = f"expected type 'str', got {type(extension)} instead"
        raise TypeError(message)

    ext = standardize_file_extension(extension)
    filename = ".".join([filepath.name, ext])
    result = filepath.parent / filename
    return result


def standardize_file_extension(extension: str) -> str:
    """Standardize file extension.

    Args:
        extension: File extension.

    Returns:
        File extension.

    Raises:
        TypeError: when `extension` is not type `str`.

    """
    if not isinstance(extension, str):
        message = f"expected type 'str', got {type(extension)} instead"
        raise TypeError(message)

    result = extension.lower().strip(".")
    return result
