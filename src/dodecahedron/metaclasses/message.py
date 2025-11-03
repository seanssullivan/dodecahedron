# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
import datetime
from typing import Any
from typing import Type
from typing import TypeVar

__all__ = ["MessageMeta"]


# Custom types
T = TypeVar("T")


class MessageMeta(abc.ABCMeta):
    """Implements a message metaclass."""

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, "__created_at__", datetime.datetime.now())
        return instance
