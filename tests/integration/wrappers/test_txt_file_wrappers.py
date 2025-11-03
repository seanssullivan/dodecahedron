# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable
from typing import Optional

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.wrappers.txt_file_wrappers import TxtFileWrapper
from dodecahedron.wrappers.txt_file_wrappers import TxtIOWrapper


def test_raises_error_when_filepath_argument_is_not_path() -> None:
    with pytest.raises(TypeError, match="expected type 'PathLike'"):
        TxtFileWrapper("failure.txt")  # type: ignore


def test_raises_error_when_encoding_argument_is_not_str(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    with pytest.raises(TypeError, match="expected type 'str'"):
        path = make_txt_file("test.txt", "")
        TxtFileWrapper(path, encoding=1)  # type: ignore


def test_raises_error_when_filepath_argument_is_a_directory(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    with pytest.raises(IsADirectoryError):
        path = make_txt_file("test.txt", "")
        TxtFileWrapper(path.parent.resolve())


def test_raises_error_when_file_does_not_have_txt_extension(
    tempdir: str,
) -> None:
    path = pathlib.Path(tempdir) / "text.csv"
    with pytest.raises(ValueError, match="not a '.txt' file"):
        TxtFileWrapper(path.resolve())


def test_opening_file_returns_txt_io_wrapper(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "")
    wrapper = TxtFileWrapper(path.resolve())
    result = wrapper.open()
    assert isinstance(result, TxtIOWrapper)


def test_returned_io_wrapper_is_not_closed(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "")
    wrapper = TxtFileWrapper(path.resolve())
    result = wrapper.open()
    assert not result.closed


def test_can_be_passed_to_builtin_open_function(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "")
    wrapper = TxtFileWrapper(path.resolve())
    open(wrapper).close()


def test_can_read_from_txt_file(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "success")
    wrapper = TxtFileWrapper(path.resolve())
    with wrapper.open() as file:
        result = file.read()

    assert result == "success"


def test_can_read_line_from_txt_file(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "success")
    wrapper = TxtFileWrapper(path.resolve())
    with wrapper.open() as file:
        result = file.readline()

    assert result == "success"


def test_can_read_lines_from_txt_file(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "result\r\nsuccess\r\n")

    wrapper = TxtFileWrapper(path.resolve())
    with wrapper.open() as file:
        results = file.readlines()

    expected = ["result\r\n", "success\r\n"]
    assert results == expected


def test_can_write_to_txt_file(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "")

    wrapper = TxtFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.write("success")

    result = path.read_text()
    assert result == "success"


def test_can_write_lines_to_txt_file(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> None:
    path = make_txt_file("test.txt", "")
    wrapper = TxtFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.writelines(["value\n", "One\n", "Two\n", "Three\n"])

    with path.open() as file:
        result = file.read()

    expected = "value\nOne\nTwo\nThree\n"
    assert result == expected
