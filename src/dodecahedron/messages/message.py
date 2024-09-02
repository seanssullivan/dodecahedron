# -*- coding: utf-8 -*-
"""Message class."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from __future__ import annotations
import abc
import datetime

__all__ = ["BaseMessage"]


# Attributes
CREATED_AT = "__created_at__"


class BaseMessage(abc.ABC):
    """Class implements a message."""

    def __new__(cls) -> BaseMessage:
        instance = super().__new__(cls)
        now = datetime.datetime.now()
        setattr(instance, CREATED_AT, now)
        return instance

    def __gt__(self, other: object) -> bool:
        result = (
            getattr(self, CREATED_AT) > getattr(other, CREATED_AT)
            if isinstance(other, BaseMessage)
            else False
        )
        return result

    def __lt__(self, other: object) -> bool:
        result = (
            getattr(self, CREATED_AT) < getattr(other, CREATED_AT)
            if isinstance(other, BaseMessage)
            else False
        )
        return result
