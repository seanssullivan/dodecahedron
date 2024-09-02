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

# Local Imports
from .metaclasses import SingletonMeta

__all__ = ["BaseMessageBroker"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


class AbstractMessageBroker(abc.ABC):
    """Represents an abstract message broker."""

    @property
    @abc.abstractmethod
    def channels(self) -> List[str]:
        """Channels."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def subscribers(self) -> Dict[str, List[Callable[[dict], Any]]]:
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
    def subscribe(
        self, channel: str, subscriber: Callable[[dict], Any]
    ) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        raise NotImplementedError


class BaseMessageBroker(AbstractMessageBroker, metaclass=SingletonMeta):
    """Implements a message broker."""

    __singleton__ = True

    def __init__(self) -> None:
        self._subscribers = defaultdict(list)

    @property
    def channels(self) -> List[str]:
        """Channels."""
        return list(self._subscribers.keys())

    @property
    def subscribers(self) -> Dict[str, List[Callable[[dict], Any]]]:
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
    def make_message(event: str, /) -> dict:
        """Make message to send to subscribers.

        Args:
            event: Published event.

        Returns:
            Message.

        """
        message = {"data": event, "created_at": datetime.now()}
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
            except Exception:
                log.exception("Exception handling %s event", channel)
                continue

    def subscribe(self, channel: str, subscriber: Callable) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        self.subscribers[channel].append(subscriber)
