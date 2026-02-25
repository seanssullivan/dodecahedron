# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from datetime import datetime
from importlib import metadata
from pathlib import Path
from packaging.version import Version
from typing import Any
from typing import Dict
from typing import Optional

# Local Imports
from .abstract_models import AbstractModel

__all__ = ["Package"]


class Package(AbstractModel):
    """Class implements a package.

    Args:
        name: Name of package.
        distribution (optional); Distribution.
        filepath (optional): Filepath.
        version (optional): Version.

    """

    def __init__(
        self,
        name: str,
        *,
        distribution: Optional[metadata.Distribution] = None,
        filepath: Optional[Path] = None,
        version: Optional[Version] = None,
    ) -> None:
        self._name = name
        self.version = version
        self.filepath = filepath
        self.distribution = distribution

        # Tracking attributes
        self._removed_at: Optional[datetime] = None

    @property
    def name(self) -> str:
        """Name of package."""
        return self._name

    @property
    def distribution(self) -> Optional[metadata.Distribution]:
        """Distribution of package."""
        return self._distribution

    @distribution.setter
    def distribution(self, value: Any) -> None:
        if value and not isinstance(value, metadata.Distribution):
            expected = "expected type 'Distribution'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._distribution = value

    @property
    def filepath(self) -> Optional[Path]:
        """Filepath for package."""
        return self._filepath

    @filepath.setter
    def filepath(self, value: Any) -> None:
        if value and not isinstance(value, Path):
            expected = "expected type 'Path'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._filepath = value
        if value is not None:
            version = get_version_from_filepath(value)
            self.version = version

    @property
    def version(self) -> Optional[Version]:
        """Version of package."""
        return self._version

    @version.setter
    def version(self, value: Any) -> None:
        if value and not isinstance(value, Version):
            expected = "expected type 'Version'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._version = value

    @property
    def is_dev_release(self) -> bool:
        """Whether version is development release."""
        result = bool(self.version.dev) if self.version else False
        return result

    @property
    def is_final_release(self) -> bool:
        """Whether version is final release."""
        result = not self.is_dev_release and not self.is_pre_release
        return result

    @property
    def is_pre_release(self) -> bool:
        """Whether version is pre-release."""
        result = bool(self.version.pre) if self.version else False
        return result

    @property
    def is_removed(self) -> bool:
        """Whether package was removed."""
        return self._removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """When package was removed."""
        return self._removed_at

    @removed_at.setter
    def removed_at(self, value: Any) -> None:
        if value and not isinstance(value, datetime):
            message = f"expected type 'datetime', got {type(value)} instead"
            raise TypeError(message)

        self._removed_at = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Package):
            return other.name == self.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Package) or other.name != self.name:
            return False

        if other.version and self.version:
            return other.version < self.version

        return False

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Package) or other.name != self.name:
            return False

        if other.version and self.version:
            return other.version > self.version

        return False

    @classmethod
    def from_distribution(cls, __dist: metadata.Distribution, /) -> Package:
        """Make package from distribution.

        Args:
            distribution: Distribution

        Returns:
            Package.

        """
        result = Package(
            # PathDistribution as no attribute 'name', name must be retrieved
            # from distribution metadata.
            __dist.metadata["Name"],
            distribution=__dist,
            version=Version(__dist.version),
        )
        return result

    def update(
        self,
        __data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Update package.

        Args:
            __data (optional): Data with which to update package.
            **kwargs: Keyword arguments.

        """
        data = __data or {}
        data.update(kwargs)

        if "version" in data:
            self.version = data["version"]

        if "filepath" in data:
            self.filepath = data["filepath"]


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_version_from_filepath(__path: Path, /) -> Optional[Version]:
    """Get version of package from filepath.

    Args:
        __path: Filepath.

    Returns:
        Version.

    """
    try:
        value = __path.stem.split("-")[1]
        result = Version(value)

    except (AttributeError, IndexError, KeyError):
        return None

    return result
