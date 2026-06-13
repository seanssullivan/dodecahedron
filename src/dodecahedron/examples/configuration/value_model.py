# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from datetime import datetime
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

# Local Imports
from dodecahedron.models import AbstractModel

if TYPE_CHECKING:
    from .section_model import ConfigurationSection

__all__ = ["ConfigurationValue"]


class ConfigurationValue(AbstractModel):
    """Class implements a configuration value.

    Args:
        reference: Reference.
        value: Value.

    """

    def __init__(
        self,
        reference: str,
        value: Optional[Any] = None,
    ) -> None:
        self._reference = reference
        self._value = value

        # Parent
        self._section: Optional["ConfigurationSection"] = None

        # Tracking attributes
        self._created_at: datetime = datetime.now()
        self._removed_at: Optional[datetime] = None
        self._updated_at: Optional[datetime] = None

    @property
    def reference(self) -> str:
        """Reference."""
        return self._reference

    @property
    def value(self) -> Optional[Any]:
        """Value."""
        return self._value

    @property
    def section(self) -> Optional["ConfigurationSection"]:
        """Section."""
        return self._section

    @property
    def created_at(self) -> datetime:
        """When value was created."""
        return self._created_at

    @property
    def is_removed(self) -> bool:
        """Whether value was removed."""
        return self._removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """When value was removed."""
        return self._removed_at

    @removed_at.setter
    def removed_at(self, value: Any) -> None:
        if value and not isinstance(value, datetime):
            message = f"expected type 'datetime', got {type(value)} instead"
            raise TypeError(message)

        self._removed_at = value

    @property
    def is_updated(self) -> bool:
        """Whether value was updated."""
        return self._updated_at is not None

    @property
    def updated_at(self) -> Optional[datetime]:
        """When value was updated."""
        return self._updated_at

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfigurationValue):
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
        """Update value.

        Args:
            __value: Value to set for value.

        """
        self._value = __value
        self._updated_at = datetime.now()
