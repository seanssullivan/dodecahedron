# -*- coding: utf-8 -*-
"""Message class."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from __future__ import annotations
import abc
import datetime

# Local Imports
from ..metaclasses import MessageMeta

__all__ = ["AbstractMessage"]


class AbstractMessage(abc.ABC, metaclass=MessageMeta):
    """Class represents an abstract message."""

    _created_at: datetime.datetime

    def __gt__(self, other: object) -> bool:
        result = (
            self._created_at > other._created_at
            if isinstance(other, AbstractMessage)
            else False
        )
        return result

    def __lt__(self, other: object) -> bool:
        result = (
            self._created_at < other._created_at
            if isinstance(other, AbstractMessage)
            else False
        )
        return result

    def __repr__(self) -> str:
        result = self.__class__.__name__
        return result

    def __str__(self) -> str:
        result = self.__class__.__name__
        return result
