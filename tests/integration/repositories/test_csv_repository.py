# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import List
from typing import Optional
from typing import Union

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.repositories import AbstractCsvRepository
from dodecahedron.wrappers import AbstractFileWrapper


class ExampleRepository(AbstractCsvRepository):
    """Example repository for testing."""

    def __init__(
        self, __file: Any, objects: Optional[List[Any]] = None
    ) -> None:
        super().__init__(__file)
        self._objects = set(objects or [])

    def __contains__(self, obj: object) -> bool:
        return obj in self._objects

    def add(self, obj: object) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, ref: Union[int, str]) -> object:
        """Get object."""
        raise NotImplementedError

    def list(self) -> List[Any]:
        """List objects."""
        raise NotImplementedError

    def remove(self, obj: object) -> None:
        """Remove object."""
        raise NotImplementedError

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""


@pytest.mark.parametrize("name", ["txt_file_wrapper", "xlsx_file_wrapper"])
def test_raises_error_when_not_a_csv_file(
    name: str, request: pytest.FixtureRequest
) -> None:
    with pytest.raises(TypeError, match="expected type 'AbstractCsvWrapper'"):
        wrapper: AbstractFileWrapper = request.getfixturevalue(name)
        ExampleRepository(wrapper)
