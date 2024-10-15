# -*- coding: utf-8 -*-
"""Message class."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from __future__ import annotations
import abc
import datetime

# Local Imports
from ..metaclasses import MessageMeta

__all__ = ["BaseMessage"]


class BaseMessage(abc.ABC, metaclass=MessageMeta):
    """Class implements a message."""

    __created_at__: datetime.datetime

    def __gt__(self, other: object) -> bool:
        result = (
            self.__created_at__ > other.__created_at__
            if isinstance(other, BaseMessage)
            else False
        )
        return result

    def __lt__(self, other: object) -> bool:
        result = (
            self.__created_at__ < other.__created_at__
            if isinstance(other, BaseMessage)
            else False
        )
        return result
