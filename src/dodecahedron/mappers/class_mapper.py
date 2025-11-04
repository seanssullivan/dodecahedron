# -*- coding: utf-8 -*-
"""Class Mapper."""

# Standard Library Imports
from contextlib import contextmanager
from typing import Any
from typing import Dict
from typing import Generator
from typing import Hashable
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

# Local Imports
from .abstract_mapper import AbstractMapper

__all__ = ["ClassMapper"]


# Custom types
T = TypeVar("T")


class ClassMapper(AbstractMapper):
    """Implements a class mapper."""

    def __init__(
        self,
        __class: Type[T],
        /,
        schema: Dict[Hashable, Any],
        properties: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        super().__init__(schema)
        self._class = __class
        self._properties = properties

        setattr(self._class, "__mapper__", self)

    @property
    def cls(self) -> Type[Any]:
        """Mapped class."""
        return self._class

    @property
    def properties(self) -> Dict[Hashable, Any]:
        """Mapped properties."""
        results = self._properties or self._get_attribute_names()
        return results

    def from_dict(self, __dict: Dict[str, Any], /) -> Any:
        """Instantiate class from dictionary.

        Args:
            __dict: Dictionary.

        Returns:
            Instance of mapped class.

        """
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, key in self.properties.items():
                converter = self._get_converter(key, direction="outward")
                value = converter(__dict[key]) if converter else __dict[key]
                setattr(result, str(attr), value)

        return result

    def from_list(self, __list: List[Any], /) -> Any:
        """Instantiate class from list.

        Args:
            __list: List.

        Returns:
            Instance of mapped class.

        """
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, idx in self.properties.items():
                converter = self._get_converter(idx, direction="outward")
                value = converter(__list[idx]) if converter else __list[idx]
                setattr(result, str(attr), value)

        return result

    def to_dict(self, __instance: Any, /) -> Dict[str, Any]:
        """Convert instance of class to dictionary.

        Args:
            __instance: Instance of mapped class.

        Returns:
            Dictionary.

        """
        result: Dict[str, Any] = {}
        for attr, key in self.properties.items():
            converter = self._get_converter(key, direction="inward")
            value = (
                converter(getattr(__instance, str(attr)))
                if converter
                else getattr(__instance, str(attr))
            )
            result[key] = value

        return result

    def to_list(self, __instance: Any, /) -> List[Any]:
        """Convert instance of class to list.

        Args:
            __instance: Instance of mapped class.

        Returns:
            List.

        """
        result: List[Any] = []
        for attr, key in sorted(self.properties.items(), key=lambda i: i[1]):
            converter = self._get_converter(key, direction="inward")
            value = (
                converter(getattr(__instance, str(attr)))
                if converter
                else getattr(__instance, str(attr))
            )
            result.append(value)

        return result


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
@contextmanager
def replace_init(__class: type) -> Generator[type, None, None]:
    """Temporarily replace the ``__init__`` method on a class.

    Args:
        __class: Class.

    Yields:
        Class.

    """
    init = getattr(__class, "__init__")
    repl = getattr(object, "__init__")

    setattr(__class, "__init__", repl)
    yield __class
    setattr(__class, "__init__", init)
