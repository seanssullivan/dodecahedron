# -*- coding: utf-8 -*-
"""Abstract Mapper."""

# Standard Library Imports
from __future__ import annotations
import abc
import collections
from typing import Any
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import Literal
from typing import Optional
from typing import Union

__all__ = ["AbstractMapper"]


# Constants
INWARD = "inward"
OUTWARD = "outward"


class AbstractMapper(abc.ABC):
    """Represents an abstract mapper."""

    def __init__(self, __schema: Dict[Hashable, Any], /) -> None:
        self._schema = _MapperSchema(__schema)

    @property
    def schema(self) -> _MapperSchema:
        """Mapped schema."""
        return self._schema

    def _get_attribute_mapper(
        self, ref: Union[int, str]
    ) -> Optional[Dict[str, Any]]:
        """Get attribute mapper.

        Args:
            ref: Reference for attribute.

        Returns:
            Attribute mapper.

        """
        result = self._schema.get_attribute_mapper(ref)
        return result

    def _get_converter(
        self,
        ref: Union[int, str],
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
        result = self._schema.get_converter(ref, direction, default=default)
        return result

    def _get_attribute_names(self) -> Dict[Hashable, str]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results = self._schema.get_attribute_names()
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
        ref: Union[int, str],
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
        self, ref: Union[int, str]
    ) -> Optional[Dict[str, Any]]:
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
