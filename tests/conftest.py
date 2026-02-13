# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import fpdf
import json
import pathlib
import shutil
import tempfile
from typing import Any
from typing import Callable
from typing import Generator
from typing import List
from typing import Optional
import zipfile

# Third-Party Imports
import pytest
import xlsxwriter  # type: ignore


@pytest.fixture
def tempdir() -> Generator[pathlib.Path, None, None]:
    """Fixture to make a temporary directory.

    Yields:
        Temporary directory.

    """
    tempdir = tempfile.mkdtemp()
    yield pathlib.Path(tempdir)
    shutil.rmtree(tempdir)


@pytest.fixture
def make_csv_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.csv` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, lines: Optional[List[Any]] = None
    ) -> pathlib.Path:
        if not isinstance(filename, str):  # type: ignore
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        with path.open("w") as file:
            writer = csv.writer(file)
            for line in lines or []:
                writer.writerow(line)

        return path

    yield _make_file


@pytest.fixture
def make_json_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.json` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, content: Any = None) -> pathlib.Path:
        if not isinstance(filename, str):  # type: ignore
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        with path.open("w") as file:
            json.dump(content or [], file)

        return path

    yield _make_file


@pytest.fixture
def make_pdf_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.pdf` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, content: str = "") -> pathlib.Path:
        if not isinstance(filename, str):  # type: ignore
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "", 16)
        pdf.cell(0, 0, content)
        pdf.output(path, "F")  # type: ignore
        return path

    yield _make_file


@pytest.fixture
def make_txt_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.txt` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, content: Optional[str] = None
    ) -> pathlib.Path:
        if not isinstance(filename, str):  # type: ignore
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        with path.open("w") as file:
            file.write(content or "")

        return path

    yield _make_file


@pytest.fixture
def make_whl_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.whl` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, content: Optional[bytes] = None
    ) -> pathlib.Path:
        if not isinstance(filename, bytes):  # type: ignore
            message = f"expected type 'bytes', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        with path.open("wb") as file:
            file.write(content or b"")

        return path

    yield _make_file


@pytest.fixture
def make_xlsx_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.xlsx` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str,
        lines: Optional[List[Any]] = None,
        *,
        sheet: Optional[str] = None,
    ) -> pathlib.Path:
        if not isinstance(filename, str):  # type: ignore
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = tempdir / filename
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet(sheet)  # type: ignore

        for row, line in enumerate(lines or []):
            for col, item in enumerate(line):
                worksheet.write(row, col, item)  # type: ignore

        workbook.close()
        return path

    yield _make_file


@pytest.fixture
def make_zip_file(
    tempdir: pathlib.Path,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.zip` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(zipname: str, filepath: pathlib.Path) -> pathlib.Path:
        if not isinstance(zipname, str):  # type: ignore
            message = f"expected type 'str', got {type(zipname)} instead"
            raise TypeError(message)

        if not isinstance(filepath, pathlib.Path):  # type: ignore
            message = f"expected type 'Path', got {type(filepath)} instead"
            raise TypeError(message)

        zippath = tempdir / zipname
        with zipfile.ZipFile(zippath, "w") as file:
            file.write(filepath, arcname=filepath.name)

        return zippath

    yield _make_file
