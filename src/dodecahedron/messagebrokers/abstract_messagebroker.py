# -*- coding: utf-8 -*-
"""Abstract Message Broker."""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Protocol

__all__ = ["AbstractMessageBroker"]


class Subscriber(Protocol):
    def __call__(self, message: Dict[str, Any], **kwargs: Any) -> None: ...


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
    def publish(self, channel: str, message: str) -> None:
        """Publish a message to a channel.

        Args:
            channel: Name of channel.
            message: JSON representation of a message.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(self, channel: str, subscriber: Subscriber) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for messages on channel.

        """
        raise NotImplementedError
