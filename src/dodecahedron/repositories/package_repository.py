# -*- coding: utf-8 -*-

# Standard Library Imports
from datetime import datetime
from importlib import metadata
from packaging.version import Version
import subprocess
from typing import Any
from typing import List
from typing import Optional

# Local Imports
from .abstract_repository import AbstractRepository
from ..models import Package

__all__ = ["PackageRepository"]


class PackageRepository(AbstractRepository):
    """Class implements a package repository."""

    def __init__(
        self,
        *args: Any,
        packages: Optional[List[Package]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._packages = set(packages or [])

    def __contains__(self, obj: Any) -> bool:
        result = obj in self._packages if isinstance(obj, Package) else False
        return result

    def add(self, obj: Any, /) -> None:
        """Add package.

        Args:
            obj: Package.

        Raises:
            TypeError: when argument is not ype ``Package``.

        """
        if not isinstance(obj, Package):
            message = f"expected type 'Package', got {type(obj)} instead"
            raise TypeError(message)

        if self.can_add(obj):
            self._packages.add(obj)

    def can_add(self, obj: Any) -> bool:
        """Check whether package can be added.

        Args:
            obj: Package.

        Raises:
            TypeError: when argument is not ype ``Package``.

        """
        if not isinstance(obj, Package):
            message = f"expected type 'Package', got {type(obj)} instead"
            raise TypeError(message)

        result = obj not in self._packages and obj.distribution is None
        return result

    def get(self, ref: str, /) -> Optional[Package]:
        """Get package.

        Args:
            ref: Reference for package.

        Returns:
            Package.

        """
        try:
            result = next(pkg for pkg in self._packages if pkg.name == ref)

        except StopIteration:
            return None

        return result

    def list(self) -> List[Package]:
        """List packages.

        Returns:
            Packages.

        """
        results = sorted(pkg for pkg in self._packages)
        return results

    def load(self) -> None:
        """Load packages from environment."""
        packages = list_packages_in_environment()
        self._packages.update(packages)

    def remove(self, obj: Any, /) -> None:
        """Remove package.

        Args:
            obj: Package.

        Raises:
            TypeError: when argument is not ype ``Package``.

        """
        if not isinstance(obj, Package):
            message = f"expected type 'Package', got {type(obj)} instead"
            raise TypeError(message)

        if obj in self._packages:
            obj.removed_at = datetime.now()

    def commit(self) -> None:
        """Commit packages in repository."""
        self._install_packages()
        self._upgrade_packages()
        self._uninstall_packages()

    def _install_packages(self) -> None:
        """Install packages."""
        for package in self.list():
            if not package.distribution:
                self._install_package(package)

    def _install_package(self, __package: Package, /) -> None:
        """Install package.

        Args:
            __package: Package.

        """
        install_package(str(__package.filepath or __package.name))
        distribution = metadata.distribution(__package.name)
        __package.distribution = distribution

    def _upgrade_packages(self) -> None:
        """Upgrade packages."""
        for package in self.list():
            if not package.distribution or not package.version:
                continue

            if package.distribution.version != package.version:
                self._upgrade_package(package)

    def _upgrade_package(self, __package: Package, /) -> None:
        """Upgrade package.

        Args:
            __package: Package.

        """
        uninstall_package(str(__package.filepath or __package.name))
        distribution = metadata.distribution(__package.name)
        __package.distribution = distribution

    def _uninstall_packages(self) -> None:
        """Uninstall packages."""
        for package in self.list():
            if package.distribution and package.is_removed:
                self._uninstall_package(package)

    def _uninstall_package(self, __package: Package, /) -> None:
        """Uninstall package.

        Args:
            __package: Package.

        """
        try:
            upgrade_package(__package.name)
            distribution = metadata.distribution(__package.name)
            __package.distribution = distribution

        except metadata.PackageNotFoundError:
            __package.distribution = None
            self._packages.discard(__package)

    def rollback(self) -> None:
        """Rollback packages in repository."""
        self._packages.clear()


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def install_package(name: str, /) -> None:
    """Install package.

    Args:
        name: Name of package.

    """
    subprocess.run(["python", "-m", "pip", "install", name])


def uninstall_package(name: str, /) -> None:
    """Uninstall package.

    Args:
        name: Name of package.

    """
    subprocess.run(["python", "-m", "pip", "uninstall", name])


def upgrade_package(name: str, /) -> None:
    """Upgrade package.

    Args:
        name: Name of package.

    """
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", name])


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_installed_package_version(name: str) -> Optional[Version]:
    """Get version of installed package.

    Args:
        name: Name of package.

    Returns:
        Version.

    """
    try:
        value = metadata.version(name)
        result = Version(value)

    except metadata.PackageNotFoundError:
        return None

    return result


def get_package_in_environment(__name: str, /) -> Optional[Package]:
    """Get package in environment.

    Args:
        __name: Name of package.

    Returns:
        Package.

    """
    try:
        distribution = metadata.distribution(__name)
        result = Package.from_distribution(distribution)

    except metadata.PackageNotFoundError:
        return None

    return result


def list_packages_in_environment() -> List[Package]:
    """List packages in environment.

    Returns:
        Packages.

    """
    results = [
        Package.from_distribution(distribution)
        for distribution in metadata.distributions()
    ]
    return results
