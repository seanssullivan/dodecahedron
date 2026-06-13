# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
import configparser
from datetime import datetime
import operator
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set

# Local Imports
from dodecahedron.models import AbstractAggregate
from dodecahedron.queues import MessageQueue
from .value_model import ConfigurationValue
from ... import errors

__all__ = ["ConfigurationSection"]


class ConfigurationSection(AbstractAggregate):
    """Class implements a section of configuration.

    Args:
        reference: Reference for section.
        values: Values in section.

    """

    def __init__(
        self,
        reference: str,
        values: Optional[Iterable[ConfigurationValue]] = None,
    ) -> None:
        self._reference = reference.upper()
        self._values = set(values or [])
        for value in self._values:
            setattr(value, "_section", self)

        # Tracking attributes
        self._created_at: datetime = datetime.now()
        self._removed_at: Optional[datetime] = None

        # Events
        self._events = MessageQueue()

    @property
    def reference(self) -> str:
        """Reference for section."""
        return self._reference

    @property
    def values(self) -> Set[ConfigurationValue]:
        """Values."""
        return self._values

    @property
    def created_at(self) -> datetime:
        """When section was created."""
        return self._created_at

    @property
    def is_removed(self) -> bool:
        """Whether section was removed."""
        return self._removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """When section was removed."""
        return self._removed_at

    @removed_at.setter
    def removed_at(self, value: Any) -> None:
        if value and not isinstance(value, datetime):
            message = f"expected type 'datetime', got {type(value)} instead"
            raise TypeError(message)

        self._removed_at = value

    @property
    def events(self) -> MessageQueue:
        """Events."""
        return self._events

    def __contains__(self, obj: Any) -> bool:
        result = (
            obj in self._values
            if isinstance(obj, ConfigurationValue)
            else False
        )
        return result

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfigurationSection):
            return other.reference == self.reference

        return False

    def __hash__(self) -> int:
        return hash(self.reference)

    def __repr__(self) -> str:
        result = "<{cls} {ref}>".format(
            cls=self.__class__.__name__,
            ref=self.reference,
        )
        return result

    @classmethod
    def from_proxy(
        cls, proxy: configparser.SectionProxy
    ) -> ConfigurationSection:
        """Instantiate configuration section from section proxy.

        Args:
            proxy: Section proxy.

        Returns:
            Section.

        """
        values = [ConfigurationValue(k, v) for k, v in proxy.items()]
        result = ConfigurationSection(proxy.name, values=values)
        return result

    def add(self, obj: Any, /) -> None:
        """Add value.

        Args:
            obj: Value.

        Raises:
            TypeError: when argument is not type ``ConfigurationValue``.

        """
        errors.raise_for_instance(obj, ConfigurationValue)
        if self.can_add(obj):
            self._values.add(obj)
            setattr(obj, "_section", self)

    def can_add(self, obj: Any) -> bool:
        """Check whether value can be added.

        Args:
            obj: Value.

        Raises:
            TypeError: when argument is not type ``ConfigurationValue``.

        """
        errors.raise_for_instance(obj, ConfigurationValue)
        result = obj not in self._values
        return result

    def get(self, ref: str) -> Optional[ConfigurationValue]:
        """Get value.

        Args:
            ref: Reference for value.

        Returns:
            Value.

        """
        try:
            result = next(
                obj
                for obj in self._values
                if ref.lower() == obj.reference.lower()
            )
        except StopIteration:
            return None

        return result

    def list(self) -> List[ConfigurationValue]:
        """List values.

        Returns:
            Values.

        """
        key = operator.attrgetter("reference")
        results = sorted(self._values, key=key)
        return results

    def remove(self, obj: Any, /) -> None:
        """Remove value.

        Args:
            obj: Value.

        Raises:
            TypeError: when argument is not type ``ConfigurationValue``.

        """
        errors.raise_for_instance(obj, ConfigurationValue)
        if obj in self._values:
            var = self.get(getattr(obj, "reference"))
            setattr(var, "_removed_at", datetime.now())
