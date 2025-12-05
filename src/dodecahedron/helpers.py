# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib
from types import ModuleType
from typing import Literal
from typing import Optional
from typing import overload

__all__ = [
    "import_module",
    "raise_for_instance",
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


def raise_for_instance(__obj: object, __class: type) -> None:
    """Raise error when object is not instance of provided class.

    Args:
        __obj: Object for which to check class.
        __class: Class for which to check.

    Raises:
        TypeError: when object is not an instance of class.

    """
    if not isinstance(__obj, __class):
        expected = f"expected type '{__class.__name__!s}'"
        actual = f"got {type(__obj)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)
