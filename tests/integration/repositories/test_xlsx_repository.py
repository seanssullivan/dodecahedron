# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.repositories import AbstractXlsxRepository
from dodecahedron.wrappers import AbstractFileWrapper


class ExampleRepository(AbstractXlsxRepository):
    """Example repository for testing."""

    def __init__(
        self, __file: typing.IO, objects: typing.Optional[list] = None
    ) -> None:
        super().__init__(__file)
        self._objects = set(objects or [])

    def __contains__(self, obj: object) -> bool:
        return obj in self._objects

    def add(self, obj: object) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, _: str) -> object:
        """Get object."""
        raise NotImplementedError

    def list(self) -> list:
        """List objects."""
        raise NotImplementedError

    def remove(self, _: object) -> None:
        """Remove object."""
        raise NotImplementedError

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""


@pytest.mark.parametrize("name", ["csv_file_wrapper", "txt_file_wrapper"])
def test_raises_error_when_not_an_xlsx_file(
    name: str, request: pytest.FixtureRequest
) -> None:
    with pytest.raises(TypeError, match="expected type 'AbstractXlsxWrapper'"):
        wrapper = request.getfixturevalue(name)  # type: AbstractFileWrapper
        ExampleRepository(wrapper)


# def test_saves_an_xlsx_file(tempdir: str) -> None:
#     temppath = pathlib.Path(tempdir)
#     filepath = temppath / "test.xlsx"
#     repo = AbstractXlsxBasedRepository(filepath)

#     obj = {"id": "1", "value": "TEST"}
#     repo.add(obj)
#     repo.commit()

#     expected = temppath / "test.xlsx"
#     assert expected.exists()


# def test_loads_an_xlsx_file(
#     make_xlsx_file: Callable[..., pathlib.Path]
# ) -> None:
#     rows = [["id", "value"], ["1", "TEST"]]
#     filepath = make_xlsx_file("test.xlsx", rows)

#     repo = AbstractXlsxBasedRepository(filepath)
#     result = repo.objects

#     expected = [{"id": "1", "value": "TEST"}]
#     assert result == expected


# def test_adds_row_to_xlsx_file(
#     make_xlsx_file: Callable[..., pathlib.Path]
# ) -> None:
#     rows = [["id", "value"], ["1", "TEST"]]
#     filepath = make_xlsx_file("test.xlsx", rows)

#     repo = AbstractXlsxBasedRepository(filepath)
#     obj = {"id": "2", "value": "SUCCESS"}
#     repo.add(obj)
#     repo.commit()

#     workbook = load_workbook(filepath, data_only=True, read_only=True)
#     worksheet = workbook.active
#     result = worksheet["B3"].value
#     assert result == "SUCCESS"


# def test_adding_rows_is_idempotent(
#     make_xlsx_file: Callable[..., pathlib.Path]
# ) -> None:
#     rows = [["id", "value"], ["1", "TEST"]]
#     filepath = make_xlsx_file("test.xlsx", rows)

#     repo = AbstractXlsxBasedRepository(filepath)
#     obj = {"id": "2", "value": "SUCCESS"}
#     repo.add(obj)
#     repo.commit()

#     repo.add(obj)
#     repo.commit()

#     workbook = load_workbook(filepath, data_only=True, read_only=True)
#     worksheet = workbook.active
#     result = worksheet["B3"].value
#     assert result == "SUCCESS"
