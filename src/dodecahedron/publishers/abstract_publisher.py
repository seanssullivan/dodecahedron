# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from dataclasses import asdict
import logging
import json
from typing import Any

# Local Imports
from ..messages import event

__all__ = ["AbstractPublisher"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


class AbstractPublisher(abc.ABC):
    """Represents an abstract publisher."""

    @property
    @abc.abstractmethod
    def connection(self) -> Any:
        """Connection."""
        raise NotImplementedError

    def publish(self, channel: str, event: event.BaseEvent, /) -> None:
        """publishes an event to an external message broker.

        Args:
            channel: Channel on which to publish event.
            event: Event to publish on external broker.

        """
        log.info("publishing: channel=%s, event=%s", channel, event)
        payload = json.dumps(asdict(event))

        getattr(self.connection, "publish")(channel, payload)
