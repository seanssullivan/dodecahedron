# -*- coding: utf-8 -*-
"""Dictionary Mapper."""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import List
from typing import Optional

# Local Imports
from .abstract_mapper import AbstractMapper
from .schema import MapperSchema
from .schema import INWARD
from .schema import OUTWARD

__all__ = ["DictMapper"]


class DictMapper(AbstractMapper):
    """Implements a dictionary mapper."""

    def __init__(
        self,
        schema: Dict[Hashable, Any],
        properties: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        super().__init__()
        self._schema = MapperSchema(schema)
        self._properties = properties

    @property
    def schema(self) -> MapperSchema:
        """Mapped schema."""
        return self._schema

    @property
    def properties(self) -> Dict[Hashable, Any]:
        """Mapped properties."""
        results = self._properties or self._get_attribute_names()
        return results

    def from_dict(self, __dict: Dict[Hashable, Any], /) -> Dict[Hashable, Any]:
        """Instantiate dictionary from dictionary.

        Args:
            __dict: Dictionary.

        Returns:
            Dictionary.

        """
        if not isinstance(__dict, dict):  # type: ignore
            message = f"expected type 'dict', got {type(__dict)} instead"
            raise TypeError(message)

        result: Dict[Hashable, Any] = {}
        for outward, inward in self.properties.items():
            converter = self._get_converter(inward, direction=INWARD)
            default = self._get_default_value(inward)
            value: Any = (
                converter(__dict[outward])
                if converter and outward in __dict
                else __dict.get(outward, default)
            )
            result[str(inward)] = value

        return result

    def from_list(self, __list: List[Any], /) -> Dict[Hashable, Any]:
        """Instantiate dictionary from list.

        Args:
            __list: List.

        Returns:
            Dictionary.

        """
        result: Dict[Hashable, Any] = {}
        for key, idx in self.properties.items():
            converter = self._get_converter(idx, direction=INWARD)
            value: Any = converter(__list[idx]) if converter else __list[idx]
            result[key] = value

        return result

    def to_dict(self, __dict: Dict[Hashable, Any], /) -> Dict[Hashable, Any]:
        """Convert instance of class to dictionary.

        Args:
            __dict: Dictionary.

        Returns:
            Dictionary.

        """
        result: Dict[Hashable, Any] = {}
        for outward, inward in self.properties.items():
            converter = self._get_converter(inward, direction=OUTWARD)
            default = self._get_default_value(inward)
            value: Any = (
                converter(__dict[inward])
                if converter and inward in __dict
                else __dict.get(inward, default)
            )
            result[str(outward)] = value

        return result

    def to_list(self, __dict: Dict[Hashable, Any], /) -> List[Any]:
        """Convert instance of class to list.

        Args:
            __dict: Dictionary.

        Returns:
            List.

        """
        result: List[Any] = []
        for key, idx in sorted(self.properties.items(), key=lambda i: i[1]):
            converter = self._get_converter(idx, direction=OUTWARD)
            default = self._get_default_value(key)
            value = (
                converter(__dict[key])
                if converter and key in __dict
                else __dict.get(key, default)
            )
            result.append(value)

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
