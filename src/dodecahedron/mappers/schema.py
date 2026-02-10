# -*- coding: utf-8 -*-
"""Schema."""

# Standard Library Imports
from __future__ import annotations
import collections
from typing import Any
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import Optional

__all__ = ["MapperSchema"]


# Constants
INWARD = "inward"
OUTWARD = "outward"


class MapperSchema(collections.UserDict):  # type: ignore
    """Implements a mapper schema.

    Args:
        __mappers: Mappers.

    """

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
        direction: str = OUTWARD,
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
        if direction not in (INWARD, OUTWARD):
            message = f"invalid direction for mapper: {direction}"
            raise ValueError(message)

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

    def get_default_value(self, ref: Hashable) -> Any:
        """Get default value.

        Args:
            ref: Reference for attribute.

        Returns:
            Default value.

        """
        try:
            mapper = self.get_attribute_mapper(ref)
            result = mapper.get("default") if mapper else None

        except KeyError:
            return None

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

    def get_attribute_names(self) -> Dict[Hashable, Hashable]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results: Dict[Hashable, Hashable] = {
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
def get_attribute_name(__mapper: Any, /) -> Optional[Hashable]:
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
