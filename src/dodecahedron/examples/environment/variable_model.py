# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from datetime import datetime
from typing import Any
from typing import Optional

# Local Imports
from dodecahedron.models import AbstractModel

__all__ = ["EnvironmentVariable"]


class EnvironmentVariable(AbstractModel):
    """Class implements an environment variable.

    Args:
        reference: Reference for variable.
        value: Value of variable.

    """

    def __init__(
        self,
        reference: str,
        value: Optional[Any] = None,
    ) -> None:
        self._reference = reference.upper()
        self._value = value

        # Tracking attributes
        self._created_at: datetime = datetime.now()
        self._removed_at: Optional[datetime] = None
        self._updated_at: Optional[datetime] = None

    @property
    def reference(self) -> str:
        """Reference for variable."""
        return self._reference

    @property
    def value(self) -> Optional[Any]:
        """Value of variable."""
        return self._value

    @property
    def created_at(self) -> datetime:
        """When variable was created."""
        return self._created_at

    @property
    def is_removed(self) -> bool:
        """Whether variable was removed."""
        return self._removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """When variable was removed."""
        return self._removed_at

    @removed_at.setter
    def removed_at(self, value: Any) -> None:
        if value and not isinstance(value, datetime):
            message = f"expected type 'datetime', got {type(value)} instead"
            raise TypeError(message)

        self._removed_at = value

    @property
    def is_updated(self) -> bool:
        """Whether variable was updated."""
        return self._updated_at is not None

    @property
    def updated_at(self) -> Optional[datetime]:
        """When variable was updated."""
        return self._updated_at

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EnvironmentVariable):
            return other.reference == self.reference

        return False

    def __hash__(self) -> int:
        return hash(self.reference)

    def __repr__(self) -> str:
        result = "<{cls} {ref} (value={value})>".format(
            cls=self.__class__.__name__,
            ref=self.reference,
            value=self.value,
        )
        return result

    def update(self, __value: Optional[Any], /) -> None:
        """Update environment variable.

        Args:
            __value: Value to set for environment variable.

        """
        self._value = __value
        self._updated_at = datetime.now()
