# -*- coding: utf-8 -*-
"""Event class.

This module defines event classes. Events are simple data structures that work as
messages in the system, transmitting instructions from one part of the system to another.
Events distribute information whenever a specific event occurs so that subsequent actions
can be performed by processes in the system which are dependent on that information.
Events are always named using past-tense verb phrases.

"""

# Local Imports
from .message import AbstractMessage

__all__ = ["AbstractEvent"]


class AbstractEvent(AbstractMessage):
    """Class represents an abstract event."""
