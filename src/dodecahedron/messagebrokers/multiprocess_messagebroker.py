# -*- coding: utf-8 -*-
"""Multiprocessing Message Broker."""

# Standard Library Imports
from __future__ import annotations
from collections import defaultdict
import functools
import logging
from multiprocessing.synchronize import Lock
from multiprocessing import Lock as make_lock
from multiprocessing import Process
from multiprocessing import Queue
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

# Local Imports
from .base_messagebroker import MessageBroker
from .abstract_messagebroker import Subscriber
from .base_messagebroker import handle_error
from ..helpers import inject_dependencies

__all__ = ["MultiprocessMessageBroker"]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Constants
IGNORE = "ignore"
RAISE = "raise"


def lock_subscriber(func: Callable[..., Any], /) -> Callable[..., Any]:
    """Lock subscriber.

    Args:
        func: Function.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(*args: Any, lock: Lock, **kwargs: Any) -> Any:
        """Wrapper applied to decorated function.

        Args:
            obj: Object to track.
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        Returns:
            Result of called function.

        """
        try:
            lock.acquire()
            result = func(*args, **kwargs)
        except Exception:
            result = None
        finally:
            lock.release()

        return result

    functools.update_wrapper(wrapper, func)
    return wrapper


class MultiprocessMessageBroker(MessageBroker):
    """Implements a multiprocesssing message broker."""

    __singleton__ = True

    def __init__(self) -> None:
        self._queue: Queue[Dict[str, Any]] = Queue()
        self._subscribers: Dict[str, List[Subscriber]] = defaultdict(list)

        self._locks: Dict[str, Lock] = defaultdict(make_lock)
        self._processes: Dict[str, Process] = {}

    @property
    def channels(self) -> List[str]:
        """Channels."""
        return list(self._subscribers.keys())

    @property
    def queue(self) -> Queue[Dict[str, Any]]:
        """Queue."""
        return self._queue

    @property
    def subscribers(self) -> Dict[str, List[Subscriber]]:
        """Subscribers."""
        return self._subscribers

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
                process = Process(target=subscriber, args=(message,))
                key = make_key(subscriber)
                self._processes[key] = process
                process.start()

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
        dependencies: Dict[str, Any] = {
            "lock": self._get_lock(subscriber),
            "queue": self._queue,
        }
        func = inject_dependencies(lock_subscriber(subscriber), dependencies)
        super().subscribe(channel, func)

    def _get_lock(self, subscriber: Subscriber) -> Lock:
        """Get lock.

        Args:
            subscriber: Subscriber.

        Returns:
            Lock.

        """
        key = make_key(subscriber)
        result = self._locks[key]
        return result


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def make_key(subscriber: Subscriber) -> str:
    """Get key for subscriber.

    Args:
        subscriber: Subscriber.

    Returns:
        Key.

    """
    module: str = getattr(subscriber, "__module__")
    name: str = getattr(subscriber, "__name__")
    result = ".".join([module, name])
    return result
