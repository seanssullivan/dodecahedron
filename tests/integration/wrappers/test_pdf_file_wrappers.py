# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.wrappers.pdf_file_wrappers import PdfFileWrapper
from dodecahedron.wrappers.pdf_file_wrappers import PdfIOWrapper


def test_raises_error_when_filepath_argument_is_not_path() -> None:
    with pytest.raises(TypeError, match="expected type 'PathLike'"):
        PdfFileWrapper("failure.pdf")


def test_raises_error_when_filepath_argument_is_a_directory(
    make_pdf_file: Callable[[str, str], pathlib.Path]
) -> None:
    with pytest.raises(IsADirectoryError):
        path = make_pdf_file("test.pdf", "")
        PdfFileWrapper(path.parent.resolve())


def test_raises_error_when_file_does_not_have_pdf_extension(
    tempdir: str,
) -> None:
    path = pathlib.Path(tempdir) / "text.txt"
    with pytest.raises(ValueError, match="not a '.pdf' file"):
        PdfFileWrapper(path.resolve())


def test_opening_file_returns_pdf_io_wrapper(
    make_pdf_file: Callable[[str, str], pathlib.Path],
) -> None:
    path = make_pdf_file("test.pdf", "")
    wrapper = PdfFileWrapper(path.resolve())
    result = wrapper.open("rb")
    assert isinstance(result, PdfIOWrapper)


@pytest.mark.parametrize("mode", ["rb", "wb"])
def test_returned_io_wrapper_is_not_closed(
    make_pdf_file: Callable[[str, str], pathlib.Path], mode: str
) -> None:
    path = make_pdf_file("test.pdf", "")
    wrapper = PdfFileWrapper(path.resolve())
    result = wrapper.open(mode)
    assert not result.closed


def test_can_be_passed_to_builtin_open_function(
    make_pdf_file: Callable[[str, str], pathlib.Path]
) -> None:
    path = make_pdf_file("test.pdf", "")
    wrapper = PdfFileWrapper(path.resolve())
    open(wrapper).close()


@pytest.mark.skip
def test_reading_file_returns_string(
    make_pdf_file: Callable[[str, str], pathlib.Path]
) -> None:
    path = make_pdf_file("test.pdf", "")
    wrapper = PdfFileWrapper(path.resolve())
    result = wrapper.read()
    assert isinstance(result, str)
