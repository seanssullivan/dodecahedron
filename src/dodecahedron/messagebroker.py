# -*- coding: utf-8 -*-
"""Message Broker."""

# Standard Library Imports
from __future__ import annotations
import abc
from collections import defaultdict
from datetime import datetime
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

# Local Imports
from .metaclasses import SingletonMeta
from . import environment

__all__ = ["MessageBroker"]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Custom types
Subscriber = Callable[[Dict[str, Any]], None]

# Constants
IGNORE = "ignore"
RAISE = "raise"


class AbstractMessageBroker(abc.ABC):
    """Represents an abstract message broker."""

    @property
    @abc.abstractmethod
    def channels(self) -> List[str]:
        """Channels."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def subscribers(self) -> Dict[str, List[Subscriber]]:
        """Subscribers."""
        raise NotImplementedError

    @abc.abstractmethod
    def publish(self, channel: str, event: str) -> None:
        """Publish an event to a channel.

        Args:
            channel: Name of channel.
            event: JSON representation of an event.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(self, channel: str, subscriber: Subscriber) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        raise NotImplementedError


class MessageBroker(AbstractMessageBroker, metaclass=SingletonMeta):
    """Implements a message broker."""

    __singleton__ = True

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Subscriber]] = defaultdict(list)

    @property
    def channels(self) -> List[str]:
        """Channels."""
        return list(self._subscribers.keys())

    @property
    def subscribers(self) -> Dict[str, List[Subscriber]]:
        """Subscribers."""
        return self._subscribers

    def publish(self, channel: str, event: str) -> None:
        """Publish an event to a channel.

        Args:
            channel: Name of channel.
            event: JSON representation of an event.

        """
        message = self.make_message(event)
        self.send_message(channel, message)

    @staticmethod
    def make_message(event: str, /) -> Dict[str, Any]:
        """Make message to send to subscribers.

        Args:
            event: Published event.

        Returns:
            Message.

        """
        message: Dict[str, Any] = {"data": event, "created_at": datetime.now()}
        return message

    def send_message(
        self, channel: str, message: Dict[str, Any]
    ) -> None:  # pylint: disable=broad-except
        """Send message to channel subscribers.

        Args:
            channel: Name of channel.
            message: Message to send to subscribers.

        """
        for subscriber in self.subscribers[channel]:
            try:
                log.debug(
                    "sending %(event)s event to subscriber %(subscriber)s",
                    {"event": channel, "subscriber": subscriber},
                )
                subscriber(message)
            except Exception as error:
                handle_error(channel, error, on_error=IGNORE)
                continue

    def subscribe(self, channel: str, subscriber: Subscriber) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        self.subscribers[channel].append(subscriber)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def handle_error(
    event: str,
    error: Exception,
    *,
    on_error: Optional[Literal["ignore", "raise"]],
) -> None:
    """Handle error raised when handling event.

    Args:
        event: Event.
        error: Error raised when handling event.
        on_error: Strategy for handling errors.

    """
    exc_info = not environment.is_production_environment()
    log.error("Error handling %s", event, exc_info=exc_info)
    if on_error == RAISE:
        raise error
