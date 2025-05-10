# -*- coding: utf-8 -*-
"""Abstract Mapper."""

# Standard Library Imports
from __future__ import annotations
import abc
import collections
import typing

__all__ = ["AbstractMapper"]


# Constants
INWARD = "inward"
OUTWARD = "outward"


class AbstractMapper(abc.ABC):
    """Represents an abstract mapper."""

    def __init__(self, __schema: typing.Dict[str, typing.Any], /) -> None:
        self._schema = _MapperSchema(__schema)

    @property
    def schema(self) -> _MapperSchema:
        """Mapped schema."""
        return self._schema

    def _get_attribute_mapper(
        self, ref: typing.Union[int, str]
    ) -> typing.Optional[dict]:
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
        ref: typing.Union[int, str],
        direction: typing.Literal["inward", "outward"] = OUTWARD,
        *,
        default: typing.Callable = lambda x: x,
    ) -> typing.Optional[typing.Callable]:
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

    def _get_attribute_names(self) -> typing.Dict[str, str]:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results = self._schema.get_attribute_names()
        return results


class _MapperSchema(collections.UserDict):
    """Implements a mapper schema."""

    def __init__(self, __mappers: typing.Dict[str, typing.Any]) -> None:
        if not isinstance(__mappers, dict):
            message = f"expected type 'dict', got {type(__mappers)} instead"
            raise TypeError(message)

        self._data = standardize_attribute_mappers(__mappers)

    @property
    def data(self) -> dict:
        """Schema data."""
        return self._data

    def get_converter(
        self,
        ref: typing.Union[int, str],
        direction: typing.Literal["inward", "outward"] = OUTWARD,
        *,
        default: typing.Callable = lambda x: x,
    ) -> typing.Optional[typing.Callable]:
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
                mapper.get("converter") or default
                if direction == OUTWARD
                else default
            )

        return result

    def get_attribute_mapper(
        self, ref: typing.Union[int, str]
    ) -> typing.Optional[dict]:
        """Get attribute mapper.

        Args:
            ref: Reference for attribute.

        Returns:
            Attribute mapper.

        """
        try:
            result = self._data[ref]
        except KeyError:
            return None

        return result

    def get_attribute_names(self) -> dict:
        """Get attribute names.

        Returns:
            Attribute names.

        """
        results = {
            get_attribute_name(attr): key for key, attr in self._data.items()
        }
        return results


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def standardize_attribute_mappers(
    __mappers: typing.Dict[str, typing.Any], /
) -> dict:
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


def standardize_attribute_mapper(__mapper: typing.Any, /) -> dict:
    """Standardize attribute mapper.

    Args:
        __mapper: Attribute mapper.

    Returns:
        Attribute mapper.

    """
    if isinstance(__mapper, dict):
        return __mapper

    if isinstance(__mapper, str):
        return {"map_to": __mapper}

    message = "invalid attribute mapper"
    raise ValueError(message)


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_attribute_name(__mapper: typing.Any, /) -> typing.Optional[str]:
    """Get mapped attribute.

    Args:
        __mapper: Attribute mapper.

    Returns:
        Mapped attribute.

    """
    if isinstance(__mapper, dict):
        return __mapper.get("map_to")

    if isinstance(__mapper, str):
        return __mapper

    return None
