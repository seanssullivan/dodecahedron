# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
import datetime
import typing

__all__ = ["MessageMeta"]


# Custom types
T = typing.TypeVar("T")


class MessageMeta(abc.ABCMeta):
    """Implements a message metaclass."""

    def __call__(cls: typing.Type[T], *args, **kwargs) -> T:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, "__created_at__", datetime.datetime.now())
        return instance
