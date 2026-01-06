# -*- coding: utf-8 -*-
"""Base Message Broker."""

# Standard Library Imports
from __future__ import annotations
from collections import defaultdict
from datetime import datetime
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

# Local Imports
from .abstract_messagebroker import AbstractMessageBroker
from .abstract_messagebroker import Subscriber
from ..metaclasses import SingletonMeta
from .. import config

__all__ = ["MessageBroker"]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Constants
IGNORE = "ignore"
RAISE = "raise"


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

    def publish(self, channel: Any, message: str) -> None:
        """Publish a message to a channel.

        Args:
            channel: Name of channel.
            message: JSON representation of a message.

        Raises:
            TypeError: when `channel` argument is not type ``str``.

        """
        if not isinstance(channel, str):
            arg = f"expected type 'str', got {type(channel)} instead"
            raise TypeError(arg)

        self.send_message(channel, self.make_message(message))

    @staticmethod
    def make_message(__data: str, /) -> Dict[str, Any]:
        """Make message to send to subscribers.

        Args:
            __data: Data to include in message.

        Returns:
            Message.

        """
        result: Dict[str, Any] = {
            "data": __data,
            "created_at": datetime.now(),
        }
        return result

    def send_message(
        self, channel: Any, message: Dict[str, Any]
    ) -> None:  # pylint: disable=broad-except
        """Send message to channel subscribers.

        Args:
            channel: Name of channel.
            message: Message to send to subscribers.

        Raises:
            TypeError: when `channel` argument is not type ``str``.

        """
        if not isinstance(channel, str):
            arg = f"expected type 'str', got {type(channel)} instead"
            raise TypeError(arg)

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

    def subscribe(self, channel: Any, subscriber: Subscriber) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for messages on channel.

        Raises:
            TypeError: when `channel` argument is not type ``str``.

        """
        if not isinstance(channel, str):
            arg = f"expected type 'str', got {type(channel)} instead"
            raise TypeError(arg)

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
    exc_info = not config.is_production_environment()
    log.error("Error handling %s", event, exc_info=exc_info)
    if on_error == RAISE:
        raise error
