# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations

# Third-Party Imports
import redis

# Local Imports
from .abstract_publisher import AbstractPublisher

__all__ = ["RedisPublisher"]


class RedisPublisher(AbstractPublisher):
    """Implements a Redis publisher.

    Attributes:
        connection: Redis connection.

    """

    def __init__(self, **kwargs) -> None:
        self._connection = redis.Redis(**kwargs)

    @property
    def connection(self) -> redis.Redis:
        """Redis connection."""
        return self._connection
