# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.wrappers.csv_file_wrappers import CsvFileWrapper
from dodecahedron.wrappers.csv_file_wrappers import CsvIOWrapper


def test_raises_error_when_filepath_argument_is_not_path() -> None:
    with pytest.raises(TypeError, match="expected type 'PathLike'"):
        CsvFileWrapper("failure.txt")


def test_raises_error_when_encoding_argument_is_not_str(
    make_csv_file: typing.Callable[[str, list], pathlib.Path],
) -> None:
    with pytest.raises(TypeError, match="expected type 'str'"):
        path = make_csv_file("test.txt", [])
        CsvFileWrapper(path, encoding=1)


def test_raises_error_when_filepath_argument_is_a_directory(
    make_csv_file: typing.Callable[[str, list], pathlib.Path],
) -> None:
    with pytest.raises(IsADirectoryError):
        path = make_csv_file("test.txt", [])
        CsvFileWrapper(path.parent.resolve())


def test_raises_error_when_file_does_not_have_csv_extension(
    tempdir: str,
) -> None:
    path = pathlib.Path(tempdir) / "text.txt"
    with pytest.raises(ValueError, match="not a '.csv' file"):
        CsvFileWrapper(path.resolve())


def test_opening_file_returns_csv_io_wrapper(
    make_csv_file: typing.Callable[[str, list], pathlib.Path],
) -> None:
    path = make_csv_file("test.csv", [])
    wrapper = CsvFileWrapper(path.resolve())
    result = wrapper.open()
    assert isinstance(result, CsvIOWrapper)


def test_returned_io_wrapper_is_not_closed(
    make_csv_file: typing.Callable[[str, list], pathlib.Path],
) -> None:
    path = make_csv_file("test.csv", [])
    wrapper = CsvFileWrapper(path.resolve())
    result = wrapper.open()
    assert not result.closed


def test_can_be_passed_to_builtin_open_function(
    make_csv_file: typing.Callable[[str, list], pathlib.Path],
) -> None:
    path = make_csv_file("test.csv", [])
    wrapper = CsvFileWrapper(path.resolve())
    open(wrapper).close()


def test_can_read_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        result = file.read()

    expected = "id,value\r\n1,One\r\n2,Two\r\n3,Three\r\n"
    assert result == expected


def test_can_read_line_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        result = file.readline()

    expected = "1,One\r\n"
    assert result == expected


def test_can_read_lines_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        results = file.readlines()

    expected = ["1,One\r\n", "2,Two\r\n", "3,Three\r\n"]
    assert results == expected


def test_can_read_record_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        result = file.read_record()

    expected = {"id": "1", "value": "One"}
    assert result == expected


def test_reading_record_sets_fieldnames(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        file.read_record()

        expected = ["id", "value"]
        assert file.fieldnames == expected


def test_can_read_records_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        results = file.read_records()

    expected = [
        {"id": "1", "value": "One"},
        {"id": "2", "value": "Two"},
        {"id": "3", "value": "Three"},
    ]
    assert results == expected


def test_reading_records_sets_fieldnames(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        file.read_records()

        expected = ["id", "value"]
        assert file.fieldnames == expected


def test_can_read_row_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve(), fieldnames=["id", "value"])
    with wrapper.open() as file:
        result = file.read_row()

    expected = ["1", "One"]
    assert result == expected


@pytest.mark.parametrize("fieldnames", [None, ["id", "value"]])
def test_reading_row_does_not_return_fieldnames(
    make_csv_file: typing.Callable[..., pathlib.Path],
    fieldnames: typing.Optional[typing.Sequence],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve(), fieldnames=fieldnames)
    with wrapper.open() as file:
        result = file.read_row()

    expected = ["1", "One"]
    assert result == expected


def test_reading_row_sets_fieldnames(
    make_csv_file: typing.Callable[..., pathlib.Path]
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        file.read_row()

        expected = ["id", "value"]
        assert file.fieldnames == expected


def test_can_read_rows_from_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve(), fieldnames=["id", "value"])
    with wrapper.open() as file:
        results = file.read_rows()

    expected = [["1", "One"], ["2", "Two"], ["3", "Three"]]
    assert results == expected


@pytest.mark.parametrize("fieldnames", [None, ["id", "value"]])
def test_reading_rows_does_not_return_headers(
    make_csv_file: typing.Callable[..., pathlib.Path],
    fieldnames: typing.Optional[typing.Sequence],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve(), fieldnames=fieldnames)
    with wrapper.open() as file:
        results = file.read_rows()

    expected = [["1", "One"], ["2", "Two"], ["3", "Three"]]
    assert results == expected


def test_reading_rows_sets_headers(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csv_file("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open() as file:
        file.read_rows()

        expected = ["id", "value"]
        assert file.fieldnames == expected


def test_can_write_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.write("id,value\r\n1,One\r\n2,Two\r\n3,Three\r\n")

    with path.open() as file:
        result = file.readlines()

    expected = ["id,value\n", "1,One\n", "2,Two\n", "3,Three\n"]
    assert result == expected


def test_can_write_lines_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.writelines(["id,value\n", "1,One\n", "2,Two\n", "3,Three\n"])

    with path.open() as file:
        result = file.read()

    expected = "id,value\n1,One\n2,Two\n3,Three\n"
    assert result == expected


def test_can_write_header_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve(), fieldnames=["id", "value"])
    with wrapper.open("w") as file:
        file.write_header()

    with path.open() as file:
        result = file.readlines()

    expected = ["id,value\n"]
    assert result == expected


def test_can_write_record_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve(), fieldnames=["id", "value"])
    with wrapper.open("w") as file:
        file.write_header()
        file.write_record({"id": "1", "value": "One"})

    with path.open() as file:
        result = file.readlines()

    expected = ["id,value\n", "1,One\n"]
    assert result == expected


def test_can_write_records_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve(), fieldnames=["id", "value"])
    with wrapper.open("w") as file:
        file.write_header()
        file.write_records(
            [
                {"id": "1", "value": "One"},
                {"id": "2", "value": "Two"},
                {"id": "3", "value": "Three"},
            ]
        )

    with path.open() as file:
        result = file.readlines()

    expected = ["id,value\n", "1,One\n", "2,Two\n", "3,Three\n"]
    assert result == expected


def test_can_write_row_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.write_row(["1", "One"])

    with path.open() as file:
        result = file.readlines()

    expected = ["1,One\n"]
    assert result == expected


def test_can_write_rows_to_csv_file(
    make_csv_file: typing.Callable[..., pathlib.Path],
) -> None:
    path = make_csv_file("test.csv")
    wrapper = CsvFileWrapper(path.resolve())
    with wrapper.open("w") as file:
        file.write_rows([["1", "One"], ["2", "Two"], ["3", "Three"]])

    with path.open() as file:
        result = file.readlines()

    expected = ["1,One\n", "2,Two\n", "3,Three\n"]
    assert result == expected
