# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import importlib
import inspect
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Literal
from typing import Optional
from typing import overload

__all__ = [
    "import_module",
    "inject_dependencies",
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


def inject_dependencies(
    __func: Callable[..., None],
    /,
    dependencies: Dict[str, Any],
) -> Callable[..., None]:
    """Inject dependencies into function.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        __func: Function.
        dependencies: Dependencies.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    params = inspect.signature(__func).parameters
    kwargs = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    result = functools.partial(__func, **kwargs)
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
