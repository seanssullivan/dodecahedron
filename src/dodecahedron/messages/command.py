# -*- coding: utf-8 -*-
"""Command class.

This module defines command classes. Commands are simple data structures that
work as messages in the system, transmitting instructions from one part of the
system to another. Commands encapsulate the intent to perform a specific
action, along with an expectation of a particular result. Commands are always
named using an imperative mood verb phrase.

Actions implemented by these commands should be restricted to write methods:
insert, update, and delete. The only time select statements should arise are
when information is required during the process of writing a record to the
database, such as retrieving the necessary database IDs for foreign keys.

"""

# Local Imports
from .message import AbstractMessage

__all__ = ["AbstractCommand"]


class AbstractCommand(AbstractMessage):
    """Class represents an abstract command."""
