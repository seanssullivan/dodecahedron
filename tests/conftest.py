# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import fpdf
import json
import pathlib
import shutil
import tempfile
import typing
import zipfile

# Third-Party Imports
import pytest
import xlsxwriter


@pytest.fixture
def tempdir() -> typing.Generator[str, None, None]:
    """Fixture to make a temporary directory.

    Yields:
        Temporary directory.

    """
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture
def make_csv_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.csv` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, lines: typing.Optional[list] = None
    ) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            writer = csv.writer(file)
            for line in lines or []:
                writer.writerow(line)

        return path

    yield _make_file


@pytest.fixture
def make_json_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.json` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, content: typing.Any = None) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            json.dump(content or [], file)

        return path

    yield _make_file


@pytest.fixture
def make_pdf_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.pdf` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, content: str = "") -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "", 16)
        pdf.cell(0, 0, content)
        pdf.output(path, "F")
        return path

    yield _make_file


@pytest.fixture
def make_txt_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.txt` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, content: typing.Optional[str] = None
    ) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            file.write(content or "")

        return path

    yield _make_file


@pytest.fixture
def make_xlsx_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.xlsx` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str,
        lines: typing.Optional[list] = None,
        *,
        sheet: typing.Optional[str] = None,
    ) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet(sheet)

        for row, line in enumerate(lines or []):
            for col, item in enumerate(line):
                worksheet.write(row, col, item)

        workbook.close()
        return path

    yield _make_file


@pytest.fixture
def make_zip_file(
    tempdir: str,
) -> typing.Generator[typing.Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary `.zip` file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(zipname: str, filepath: pathlib.Path) -> pathlib.Path:
        if not isinstance(zipname, str):
            message = f"expected type 'str', got {type(zipname)} instead"
            raise TypeError(message)

        if not isinstance(filepath, pathlib.Path):
            message = f"expected type 'Path', got {type(filepath)} instead"
            raise TypeError(message)

        zippath = pathlib.Path(tempdir) / zipname
        with zipfile.ZipFile(zippath, "w") as file:
            file.write(filepath, arcname=filepath.name)

        return zippath

    yield _make_file
