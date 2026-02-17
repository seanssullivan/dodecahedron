# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib
from importlib import metadata
from packaging.version import Version
from types import ModuleType
from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from typing import overload

__all__ = [
    "get_installed_package_version",
    "import_module",
    "is_final_release",
    "is_prerelease",
    "list_installed_packages",
    "search_installed_packages",
]


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


# ----------------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------------
def is_final_release(__version: Any, /) -> bool:
    """Check whether version is final release.

    Args:
        __version: Version.

    Returns:
        Whether version is final release.

    Raises:
        TypeError: when argument is not type `Version`.

    """
    if not isinstance(__version, Version):
        message = f"expected type 'Version', got {type(__version)} instead"
        raise TypeError(message)

    result = not __version.dev and not __version.pre
    return result


def is_prerelease(__version: Any, /) -> bool:
    """Check whether version is pre-release.

    Args:
        __version: Version.

    Returns:
        Whether version is pre-release.

    Raises:
        TypeError: when argument is not type `Version`.

    """
    if not isinstance(__version, Version):
        message = f"expected type 'Version', got {type(__version)} instead"
        raise TypeError(message)

    result = bool(__version.pre)
    return result
