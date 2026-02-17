# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib
from importlib import metadata
from packaging.version import Version
from types import ModuleType
from typing import List
from typing import Literal
from typing import Optional
from typing import overload

__all__ = [
    "get_package_version",
    "import_module",
    "list_installed_packages",
    "search_installed_packages",
]


def get_package_version(name: str) -> Optional[Version]:
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


@overload
def import_module(
    name: str,
    package: Optional[str] = None,
    *,
    required: Literal[True] = True,
) -> ModuleType: ...


@overload
def import_module(
    name: str,
    package: Optional[str] = None,
    *,
    required: Literal[False] = False,
) -> Optional[ModuleType]: ...


def import_module(
    name: str,
    package: Optional[str] = None,
    *,
    required: bool = True,
) -> Optional[ModuleType]:
    """Import module.

    Args:
        name: Name of module.
        package (optional): Package. Default ``None``.
        required: Whether package is required. Default ``True``.

    Returns:
        Module.

    """
    try:
        result = importlib.import_module(name, package)

    except (ImportError, ModuleNotFoundError) as error:
        if required is True:
            raise error

        return None

    return result


def list_installed_packages() -> List[str]:
    """List installed packages.

    Returns:
        Packages.

    """
    results = sorted(dist.name for dist in metadata.distributions())
    return results


def search_installed_packages(*args: str) -> List[str]:
    """Search installed packages.

    Args:
        args: Reference(s) for packages.

    Returns:
        Packages.

    """
    results = [
        name
        for name in list_installed_packages()
        if all(arg in name for arg in args)
    ]
    return results
