# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.repositories import AbstractTxtRepository
from dodecahedron.wrappers import AbstractFileWrapper


class ExampleRepository(AbstractTxtRepository):
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


@pytest.mark.parametrize("name", ["csv_file_wrapper", "xlsx_file_wrapper"])
def test_raises_error_when_not_a_txt_file(
    name: str, request: pytest.FixtureRequest
) -> None:
    with pytest.raises(TypeError, match="expected type 'AbstractTxtWrapper'"):
        wrapper = request.getfixturevalue(name)  # type: AbstractFileWrapper
        ExampleRepository(wrapper)
