# -*- coding: utf-8 -*-

# Standard Library Imports
import pathlib
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron import wrappers


@pytest.fixture
def csv_file_wrapper(
    make_csv_file: Callable[[str, Optional[List[Any]]], pathlib.Path],
) -> wrappers.CsvFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_csv_file("test.csv", [])
    result = wrappers.CsvFileWrapper(path)
    return result


@pytest.fixture
def txt_file_wrapper(
    make_txt_file: Callable[[str, Optional[str]], pathlib.Path],
) -> wrappers.TxtFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_txt_file("test.txt", "")
    result = wrappers.TxtFileWrapper(path)
    return result


@pytest.fixture
def xlsx_file_wrapper(
    make_xlsx_file: Callable[[str, Optional[List[Any]]], pathlib.Path],
) -> wrappers.XlsxFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_xlsx_file("test.xlsx", [])
    result = wrappers.XlsxFileWrapper(path)
    return result
