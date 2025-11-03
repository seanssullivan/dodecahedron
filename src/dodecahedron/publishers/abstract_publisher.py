# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from dataclasses import asdict
from dataclasses import is_dataclass
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
        data = asdict(event) if is_dataclass(event) else event
        payload = json.dumps(data)

        getattr(self.connection, "publish")(channel, payload)
