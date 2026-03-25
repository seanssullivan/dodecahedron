# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from dataclasses import asdict
from dataclasses import is_dataclass
import logging
import json
from typing import Any

# Local Imports
from ..json import JSONEncoder
from ..messages import AbstractMessage

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

    def publish(self, channel: str, message: AbstractMessage, /) -> None:
        """publishes an message to an external message broker.

        Args:
            channel: Channel on which to publish message.
            message: Message to publish on external broker.

        """
        log.info("publishing: channel=%s, message=%s", channel, message)
        data = asdict(message) if is_dataclass(message) else message
        payload = json.dumps(data, cls=JSONEncoder)
        getattr(self.connection, "publish")(channel, payload)
