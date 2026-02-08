# -*- coding: utf-8 -*-
"""Class Mapper."""

# Standard Library Imports
from __future__ import annotations
from contextlib import contextmanager
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Generic
from typing import Hashable
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

# Local Imports
from .abstract_mapper import AbstractMapper
from .schema import MapperSchema
from .schema import INWARD
from .schema import OUTWARD

__all__ = ["ClassMapper"]


# Custom types
T = TypeVar("T")


class ClassMapper(AbstractMapper, Generic[T]):
    """Implements a class mapper."""

    def __init__(
        self,
        __class: Type[T],
        /,
        schema: Dict[Hashable, Any],
        properties: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        super().__init__()
        self._class = __class
        self._schema = MapperSchema(schema)
        self._properties = properties

        setattr(self._class, "_mapper", self)

    @property
    def cls(self) -> Type[T]:
        """Mapped class."""
        return self._class

    @property
    def schema(self) -> MapperSchema:
        """Mapped schema."""
        return self._schema

    @property
    def properties(self) -> Dict[Hashable, Any]:
        """Mapped properties."""
        results = self._properties or self._get_attribute_names()
        return results

    def from_dict(self, __dict: Dict[Hashable, Any], /) -> T:
        """Instantiate class from dictionary.

        Args:
            __dict: Dictionary.

        Returns:
            Instance of mapped class.

        """
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, key in self.properties.items():
                converter = self._get_converter(key, direction=INWARD)
                default = self._get_default_value(key)
                value = (
                    converter(__dict[key])
                    if converter and key in __dict
                    else __dict.get(key, default)
                )
                setattr(result, str(attr), value)

        return result

    def from_list(self, __list: List[Any], /) -> T:
        """Instantiate class from list.

        Args:
            __list: List.

        Returns:
            Instance of mapped class.

        """
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, idx in self.properties.items():
                converter = self._get_converter(idx, direction=INWARD)
                value = converter(__list[idx]) if converter else __list[idx]
                setattr(result, str(attr), value)

        return result

    def to_dict(self, __instance: T, /) -> Dict[Hashable, Any]:
        """Convert instance of class to dictionary.

        Args:
            __instance: Instance of mapped class.

        Returns:
            Dictionary.

        """
        result: Dict[Hashable, Any] = {}
        for attr, key in self.properties.items():
            converter = self._get_converter(key, direction=OUTWARD)
            default = self._get_default_value(key)
            value = (
                converter(getattr(__instance, str(attr)))
                if converter and hasattr(__instance, str(attr))
                else getattr(__instance, str(attr), default)
            )
            result[key] = value

        return result

    def to_list(self, __instance: T, /) -> List[Any]:
        """Convert instance of class to list.

        Args:
            __instance: Instance of mapped class.

        Returns:
            List.

        """
        result: List[Any] = []
        for attr, key in sorted(self.properties.items(), key=lambda i: i[1]):
            converter = self._get_converter(key, direction=OUTWARD)
            default = self._get_default_value(key)
            value = (
                converter(getattr(__instance, str(attr)))
                if converter and hasattr(__instance, str(attr))
                else getattr(__instance, str(attr), default)
            )
            result.append(value)

        return result

    def _get_attribute_mapper(
        self, ref: Hashable
    ) -> Optional[Dict[Hashable, Any]]:
        """Get attribute mapper.

        Args:
            ref: Reference for attribute.

        Returns:
            Attribute mapper.

        """
        result = self.schema.get_attribute_mapper(ref)
        return result

    def _get_converter(
        self,
        ref: Hashable,
        direction: str,
        *,
        default: Callable[..., Any] = lambda x: x,  # type: ignore
    ) -> Optional[Callable[..., Any]]:
        """Get converter.

        Args:
            ref: Reference for attribute.
            direction: Direction of converter.
            default (optional): Default converter. Default `lambda x: x`.

        Returns:
            Converter.

        """
        result = self.schema.get_converter(ref, direction, default=default)
        return result

    def _get_attribute_names(self) -> Dict[Hashable, Hashable]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results = self.schema.get_attribute_names()
        return results

    def _get_default_value(self, ref: Hashable) -> Any:
        """Get default value.

        Args:
            ref: Reference for attribute.

        Returns:
            Default value.

        """
        result = self.schema.get_default_value(ref)
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
