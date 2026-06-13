# -*- coding: utf-8 -*-

# Standard Library Imports
import configparser
from datetime import datetime
import operator
import os
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

# Local Imports
from ...repositories.abstract_repository import AbstractRepository
from .section_model import ConfigurationSection
from .value_model import ConfigurationValue
from ... import errors

__all__ = ["ConfigurationRepository"]


class ConfigurationRepository(AbstractRepository):
    """Class implements a configuration repository.

    Args:
        *args (optional): Positional arguments.
        **kwargs (optional): Keyword arguments.

    """

    def __init__(
        self,
        filepath: Union["os.PathLike[Any]", str],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._filepath = filepath
        self._session = configparser.ConfigParser()
        self._session.read(self._filepath)
        self.load()

        # Tracking attributes
        self._committed_at: datetime = datetime.now()

    def __contains__(self, obj: Any) -> bool:
        result = (
            obj in self._objects
            if isinstance(obj, ConfigurationSection)
            else False
        )
        return result

    def add(self, obj: Any, /) -> None:
        """Add section to configuration.

        Args:
            obj: Section.

        """
        errors.raise_for_instance(obj, ConfigurationSection)
        if self.can_add(obj):
            self._objects.add(obj)

    def can_add(self, obj: Any) -> bool:
        """Check whether section can be added.

        Args:
            obj: Section.

        """
        errors.raise_for_instance(obj, ConfigurationSection)
        result = obj not in self._objects
        return result

    def get(self, ref: str) -> Optional[ConfigurationSection]:
        """Get section of configuration.

        Args:
            ref: Reference for section.

        Returns:
            Section.

        """
        try:
            result = next(
                obj
                for obj in self._objects
                if ref.upper() == obj.reference.upper()
            )
        except StopIteration:
            return None

        return result

    def list(self) -> List[ConfigurationSection]:
        """List sections in configuration.

        Returns:
            Sections.

        """
        key = operator.attrgetter("reference")
        results = sorted(self._objects, key=key)
        return results

    def remove(self, obj: Any, /) -> None:
        """Remove section.

        Args:
            obj: Section.

        """
        errors.raise_for_instance(obj, ConfigurationSection)
        if obj in self._objects:
            var = self.get(getattr(obj, "reference"))
            setattr(var, "_removed_at", datetime.now())

    def commit(self) -> None:
        """Commit sections in repository."""
        self._add_sections_to_configuration()
        self._add_values_to_configuration()
        self._update_values_in_configuration()
        self._remove_values_from_configuration()
        self._remove_sections_from_configuration()
        self._committed_at = datetime.now()
        self.save()

    def _add_sections_to_configuration(self) -> None:
        """Add sections to configuration."""
        key = operator.attrgetter("created_at")
        for obj in sorted(self._objects, key=key):
            if obj.created_at > self._committed_at:
                self._session[obj.reference] = {}

    def _add_values_to_configuration(self) -> None:
        """Add values to configuration."""
        key = operator.attrgetter("created_at")
        values = [value for obj in self._objects for value in obj.values]
        for value in sorted(values, key=key):
            proxy = self._session[getattr(value.section, "reference")]
            if value.created_at > self._committed_at:
                proxy[value.reference] = str(value.value)

    def _remove_sections_from_configuration(self) -> None:
        """Remove sections from configuration."""
        key = operator.attrgetter("removed_at")
        removed_sections = [obj for obj in self._objects if obj.is_removed]
        for obj in sorted(removed_sections, key=key):
            if obj.removed_at and obj.removed_at > self._committed_at:
                del self._session[obj.reference]

    def _remove_values_from_configuration(self) -> None:
        """Remove values from configuration."""
        key = operator.attrgetter("removed_at")
        removed_values = get_removed_values(self._objects)
        for value in sorted(removed_values, key=key):
            proxy = self._session[getattr(value.section, "reference")]
            if value.removed_at and value.removed_at > self._committed_at:
                del proxy[value.reference]

    def _update_values_in_configuration(self) -> None:
        """Update values to configuration."""
        key = operator.attrgetter("updated_at")
        updated_values = get_updated_values(self._objects)
        for value in sorted(updated_values, key=key):
            proxy = self._session[getattr(value.section, "reference")]
            if value.updated_at and value.updated_at > self._committed_at:
                proxy[value.reference] = str(value.value)

    def rollback(self) -> None:
        """Rollback values in repository."""
        self.load()

    def load(self) -> None:
        """Load environment variables."""
        self._objects = set(
            ConfigurationSection.from_proxy(self._session[name])
            for name in self._session.sections()
        )

    def save(self) -> None:
        """Save sections in configuration file."""
        with open(self._filepath, "w") as configfile:
            self._session.write(configfile)


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_removed_values(
    __sections: Iterable[ConfigurationSection],
) -> List[ConfigurationValue]:
    """Get removed values.

    Args:
        __sections: Sections.

    Returns:
        Values.

    """
    results = [v for obj in __sections for v in obj.values if v.is_removed]
    return results


def get_updated_values(
    __sections: Iterable[ConfigurationSection],
) -> List[ConfigurationValue]:
    """Get updated values.

    Args:
        __sections: Sections.

    Returns:
        Values.

    """
    results = [v for obj in __sections for v in obj.values if v.is_updated]
    return results
