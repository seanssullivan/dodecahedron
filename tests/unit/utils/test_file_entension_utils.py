# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import file_extension_utils as utils


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_returns_true_when_filename_has_extension(extension: str) -> None:
    result = utils.has_extension(f"test{extension!s}", extension)
    assert result is True


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_returns_true_when_filepath_has_extension(extension: str) -> None:
    filepath = pathlib.Path(f"test{extension!s}")
    result = utils.has_extension(filepath, extension)
    assert result is True


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_returns_true_when_filename_extension_can_be_anything(
    extension: str,
) -> None:
    result = utils.has_extension(f"test{extension!s}", "*")
    assert result is True


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_returns_true_when_filepath_extension_can_be_anything(
    extension: str,
) -> None:
    filepath = pathlib.Path(f"test{extension!s}")
    result = utils.has_extension(filepath, "*")
    assert result is True


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_raises_error_when_unexpected_extension_found_in_filename(
    extension: str,
) -> None:
    with pytest.raises(ValueError):
        utils.raise_for_extension("test.zip", extension)


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_raises_error_when_unexpected_extension_found_in_filepath(
    extension: str,
) -> None:
    filepath = pathlib.Path("test.zip")
    with pytest.raises(ValueError):
        utils.raise_for_extension(filepath, extension)


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_does_not_raise_error_when_filename_can_contain_any_extension(
    extension: str,
) -> None:
    utils.raise_for_extension(f"test{extension!s}", "*")


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_does_not_raise_error_when_filepath_can_contain_any_extension(
    extension: str,
) -> None:
    filepath = pathlib.Path(f"test{extension!s}")
    utils.raise_for_extension(filepath, "*")


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_sets_extension_on_filename(extension: str) -> None:
    result = utils.set_extension("test.replace", extension)
    assert result.endswith(extension)


@pytest.mark.parametrize("extension", [".csv", ".pdf", ".txt", ".xlsx"])
def test_sets_extension_on_filepath(extension: str) -> None:
    filepath = pathlib.Path("test.replace")
    result = utils.set_extension(filepath, extension)
    assert result.suffix == extension
