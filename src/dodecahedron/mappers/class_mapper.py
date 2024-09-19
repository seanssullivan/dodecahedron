# -*- coding: utf-8 -*-
"""Class Mapper."""

# Standard Library Imports
from contextlib import contextmanager
import typing

# Local Imports
from .abstract_mapper import AbstractClassMapper

__all__ = ["ClassMapper"]


# Custom types
T = typing.TypeVar("T")


class ClassMapper(AbstractClassMapper):
    """Implements a class mapper."""

    def __init__(
        self,
        __class: typing.Type[T],
        schema: typing.Any,
        properties: typing.Dict[str, typing.Any],
    ) -> None:
        self._class = __class
        self._schema = schema
        self._properties = properties

        setattr(self._class, "__mapper__", self)

    @property
    def cls(self) -> typing.Type[T]:
        """Mapped class."""
        return self._class

    @property
    def schema(self) -> typing.Dict[str, typing.Any]:
        """Mapped schema."""
        return self._schema

    @property
    def properties(self) -> typing.Dict[str, typing.Any]:
        """Mapped properties."""
        return self._properties

    def from_dict(self, __dict: dict) -> T:
        """Instantiate class from dictionary."""
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, key in self.properties.items():
                setattr(result, attr, __dict[key])

        return result

    def from_list(self, __list: list) -> T:
        """Instantiate class from list."""
        with replace_init(self.cls) as cls:
            result = cls()
            for attr, index in self.properties.items():
                setattr(result, attr, __list[index])

        return result

    def to_dict(self, __instant: T) -> dict:
        """Convert instance of class to dictionary."""
        result = {
            key: getattr(__instant, attr)
            for attr, key in self.properties.items()
        }
        return result

    def to_list(self, __instant: T) -> list:
        """Convert instance of class to list."""
        result = [
            getattr(__instant, attr)
            for attr in sorted(self.properties.items(), key=lambda i: i[1])
        ]
        return result


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
@contextmanager
def replace_init(__class: type) -> typing.Generator[type, None, None]:
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
