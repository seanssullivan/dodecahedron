# -*- coding: utf-8 -*-
# chemsys/adapters/listeners/redis_listener.py

# Standard Library Imports
from __future__ import annotations
import atexit
import logging
from typing import Callable

# Third-Party Imports
import redis

# Local Imports
from .abstract_listener import AbstractListener

__all__ = ["RedisListener"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


class RedisListener(AbstractListener):
    """Implements a Redis listener."""

    def __init__(self, **kwargs) -> None:
        self._connection = redis.Redis(**kwargs)
        self._pubsub = self._connection.pubsub(ignore_subscribe_messages=True)
        self._thread = None

    def start(self) -> None:
        """Start Redis listen."""
        self._thread = self._pubsub.run_in_thread(sleep_time=0.001)
        atexit.register(self._thread.stop)

    def stop(self) -> None:
        """Stop Redis listener."""
        self._thread.stop()
        atexit.unregister(self._thread.stop)
        self._thread = None

    def subscribe(self, **kwargs: Callable[[str, Callable], None]) -> None:
        """Subscribe event consumers.

        Args:
            **kwargs: Keyword arguments.

        """
        self._pubsub.subscribe(**kwargs)
