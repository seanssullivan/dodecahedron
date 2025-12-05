# -*- coding: utf-8 -*-
"""Class Mapper."""

# Standard Library Imports
from __future__ import annotations
import collections
from contextlib import contextmanager
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Generic
from typing import Hashable
from typing import List
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar

# Local Imports
from .abstract_mapper import AbstractMapper

__all__ = ["ClassMapper"]


# Custom types
T = TypeVar("T")

# Constants
INWARD = "inward"
OUTWARD = "outward"


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
        self._schema = _MapperSchema(schema)
        self._properties = properties

        setattr(self._class, "__mapper__", self)

    @property
    def cls(self) -> Type[T]:
        """Mapped class."""
        return self._class

    @property
    def schema(self) -> _MapperSchema:
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
                converter = self._get_converter(key, direction=OUTWARD)
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
                converter = self._get_converter(idx, direction=OUTWARD)
                value = converter(__list[idx]) if converter else __list[idx]
                setattr(result, str(attr), value)

        return result

    def to_dict(self, __instance: Any, /) -> Dict[Hashable, Any]:
        """Convert instance of class to dictionary.

        Args:
            __instance: Instance of mapped class.

        Returns:
            Dictionary.

        """
        result: Dict[Hashable, Any] = {}
        for attr, key in self.properties.items():
            converter = self._get_converter(key, direction=INWARD)
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
            converter = self._get_converter(key, direction=INWARD)
            value = (
                converter(getattr(__instance, str(attr)))
                if converter
                else getattr(__instance, str(attr))
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
        direction: Literal["inward", "outward"] = OUTWARD,
        *,
        default: Callable[..., Any] = lambda x: x,  # type: ignore
    ) -> Optional[Callable[..., Any]]:
        """Get converter.

        Args:
            ref: Reference for attribute.
            direction (optional): Direction of converter. Default ``outward``.
            default (optional): Default converter. Default `lambda x: x`.

        Returns:
            Converter.

        """
        result = self.schema.get_converter(ref, direction, default=default)
        return result

    def _get_attribute_names(self) -> Dict[Hashable, str]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results = self.schema.get_attribute_names()
        return results


class _MapperSchema(collections.UserDict):  # type: ignore
    """Implements a mapper schema."""

    def __init__(self, __mappers: Dict[Hashable, Any]) -> None:
        if not isinstance(__mappers, dict):  # type: ignore
            message = f"expected type 'dict', got {type(__mappers)} instead"
            raise TypeError(message)

        self._data = standardize_attribute_mappers(__mappers)

    @property
    def data(self) -> Dict[Hashable, Any]:  # type: ignore
        """Schema data."""
        return self._data

    def get_converter(
        self,
        ref: Hashable,
        direction: Literal["inward", "outward"] = OUTWARD,
        *,
        default: Callable[..., Any] = lambda x: x,  # type: ignore
    ) -> Optional[Callable[..., Any]]:
        """Get converter.

        Args:
            ref: Reference for attribute.
            direction (optional): Direction of converter. Default ``outward``.
            default (optional): Default converter. Default `lambda x: x`.

        Returns:
            Converter.

        """
        try:
            mapper = self.get_attribute_mapper(ref)
            result = mapper["converters"][direction] if mapper else None

        except KeyError:
            result = (
                mapper.get("converter") or default  # type: ignore
                if direction == OUTWARD
                else default
            )

        return result

    def get_attribute_mapper(
        self, ref: Hashable
    ) -> Optional[Dict[Hashable, Any]]:
        """Get attribute mapper.

        Args:
            ref: Reference for attribute.

        Returns:
            Attribute mapper.

        """
        try:
            result = self.data[ref]
        except KeyError:
            return None

        return result

    def get_attribute_names(self) -> Dict[Hashable, str]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results: Dict[Hashable, str] = {
            get_attribute_name(attr): key
            for key, attr in self.data.items()
            if get_attribute_name(attr) is not None
        }  # type: ignore
        return results


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


def standardize_attribute_mappers(
    __mappers: Dict[Hashable, Any], /
) -> Dict[Hashable, Any]:
    """Standardize attribute mappers.

    Args:
        __mappers: Attribute mappers.

    Returns:
        Attribute mappers.

    """
    results = {
        key: standardize_attribute_mapper(value)
        for key, value in __mappers.items()
    }
    return results


def standardize_attribute_mapper(__mapper: Any, /) -> Dict[Hashable, Any]:
    """Standardize attribute mapper.

    Args:
        __mapper: Attribute mapper.

    Returns:
        Attribute mapper.

    """
    if isinstance(__mapper, dict):
        return __mapper  # type: ignore

    if isinstance(__mapper, str):
        return {"map_to": __mapper}

    message = "invalid attribute mapper"
    raise ValueError(message)


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_attribute_name(__mapper: Any, /) -> Optional[str]:
    """Get mapped attribute.

    Args:
        __mapper: Attribute mapper.

    Returns:
        Mapped attribute.

    """
    if isinstance(__mapper, dict):
        return __mapper.get("map_to")  # type: ignore

    if isinstance(__mapper, str):
        return __mapper

    return None
