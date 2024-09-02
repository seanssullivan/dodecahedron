# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
import abc
import inspect
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

__all__ = ["SingletonMeta"]


# Custom types
T = TypeVar("T")


class SingletonMeta(abc.ABCMeta):
    """Implements a singleton metaclass.

    The singleton metaclass allows subclasses to act as singletons.

    By implementing the singleton pattern using a metaclass, instead of within
    the `__new__` method, we avoid calling `__init__` each time a subclass is
    instantiated.

    Notes:
        * Subclasses will only behave as singletons when they contain a
        `__singleton__` attribute which is set to ``True``.

    """

    __instances__: Dict[str, T] = {}

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        key = make_key(cls)

        if key not in SingletonMeta.__instances__:
            instance = super().__call__(*args, **kwargs)
            if SingletonMeta.is_singleton(instance):
                SingletonMeta.__instances__[key] = instance
        else:
            instance = SingletonMeta.__instances__[key]

        return instance

    @staticmethod
    def clear() -> None:
        """Clear all instances of subclasses."""
        SingletonMeta.__instances__.clear()

    @staticmethod
    def discard(__subclass: Union[object, type]) -> None:
        """Discard an instance of a subclass.

        Args:
            __subclass: Subclass to discard.

        """
        subclass = get_class(__subclass)
        key = make_key(subclass)
        if SingletonMeta.__instances__.get(key):
            del SingletonMeta.__instances__[key]

    @staticmethod
    def is_singleton(__obj: Union[object, type], /) -> bool:
        """Checks whether an object is a singleton.

        Args:
            __obj: Object.

        Returns:
            Whether object is a singleton.

        """
        result = getattr(__obj, "__singleton__", False)  # type: bool
        return result


def make_key(__cls: type, /) -> str:
    """Make a unique key for a class.

    Args:
        __cls: Class for which to make key.

    Returns:
        Key.

    """
    result = "%s.%s" % (__cls.__module__, __cls.__name__)
    return result


def get_class(__class_or_object: Any, /) -> type:
    """Get class of object.

    Args:
        __class_or_object: Class or instance.

    Returns:
        Class.

    """
    result = (
        # Unwrap argument in case class is decorated.
        inspect.unwrap(__class_or_object).__class__
        if not inspect.isclass(__class_or_object)
        else __class_or_object
    )
    return result
