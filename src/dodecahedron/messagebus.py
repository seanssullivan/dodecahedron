# -*- coding: utf-8 -*-
"""Message Bus.

This module defines message-bus classes which delivers commands and events
to their respective handlers.

Commands are simple data structures that capture an intent for the system to
perform a particular action: commands are always matched to a single handler.
When a command is executed, there is an expectation that an event will occur
as a result; whenever a process fails, the process or user that created the
command must receive an error message containing pertinent information.

Events are data structures that are broadcast to all subscribed listeners.
Events are never assigned to dedicated event handlers. Instead, handlers are
registered with the message bus and wait for an event to occur before
performing a particular action. Events reflect business logic described in
terms of 'if this happens, then do that'. They are used to implement workflows
in the system.

Implementation based on 'Architecture Patterns in Python' message-bus pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
import abc
import logging
from operator import methodcaller
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Type

# Local Imports
from .messages import BaseCommand
from .messages import BaseEvent
from .messages import AbstractMessage
from .queues import MessageQueue
from .units_of_work import AbstractUnitOfWork
from . import config

__all__ = [
    "AbstractMessageBus",
    "MessageBus",
]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Custom types
Handler = Callable[..., None]
CommandHandlers = Dict[Type[BaseCommand], Handler]
EventHandlers = Dict[Type[BaseEvent], List[Handler]]

# Constants
eventcollector = methodcaller("collect_events")
IGNORE = "ignore"
RAISE = "raise"


class AbstractMessageBus(abc.ABC):
    """Represents an abstract message bus.

    Attributes:
        uow: Unit of work.
        queue: Message queue.

    """

    @property
    @abc.abstractmethod
    def uow(self) -> AbstractUnitOfWork:
        """Unit of work."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def queue(self) -> MessageQueue:
        """Message queue."""
        raise NotImplementedError

    @abc.abstractmethod
    def handle(
        self,
        message: AbstractMessage,
        /,
        callback: Optional[Callable[..., Any]] = None,
    ) -> None:
        """Handle a message.

        Args:
            message: Message to handle.
            callback (optional): Function to call after handling message. Default ``None``.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(
        self, message: Type[AbstractMessage], handler: Handler
    ) -> None:
        """Subscribe a handler for a `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.

        """
        raise NotImplementedError


class MessageBus(AbstractMessageBus):
    """Implements a message buse.

    Args:
        uow: Unit of work.
        command_handlers: Dictionary of commands and handlers.
            Each command is associated with a single handler.
        event_handlers: Dictionary of events and handlers.
            Each event is associated with multiple handlers.

    Attributes:
        uow: Unit of work.
        queue: Message queue.

    """

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        /,
        command_handlers: CommandHandlers,
        event_handlers: EventHandlers,
    ) -> None:
        self._uow = uow
        self._command_handlers = command_handlers
        self._event_handlers = event_handlers
        self._queue = MessageQueue()

    @property
    def uow(self) -> AbstractUnitOfWork:
        """Unit of work."""
        return self._uow

    @property
    def queue(self) -> MessageQueue:
        """Message queue."""
        return self._queue

    def handle(
        self,
        message: AbstractMessage,
        /,
        callback: Optional[Callable[..., Any]] = None,
    ) -> None:
        """Handle message.

        Provided message is passed to an appropriate handler function.

        Args:
            message: Message.
            callback (optional): Function to call after handling message. Default ``None``.

        """
        if not isinstance(message, AbstractMessage):  # type: ignore
            expected = "expected type 'AbstractMessage'"
            actual = f"got {type(message)} instead"
            error = ", ".join([expected, actual])
            raise TypeError(error)

        self.queue.append(message)
        while self.queue:
            message = self.queue.popleft()
            self._handle_message(message)

        if callback is not None:
            callback()

    def subscribe(
        self,
        message: Type[AbstractMessage],
        handler: Handler,
    ) -> None:
        """Subscribe handler to `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.
            handler: Handler function to subscribe.

        """
        if not issubclass(message, (BaseCommand, BaseEvent)):
            msg = f"{type(message)} was not a 'Command' or an 'Event'"
            raise TypeError(msg)

        if issubclass(message, BaseCommand):
            self._command_handlers[message] = handler

        if issubclass(message, BaseEvent):
            self._event_handlers.setdefault(message, [])
            self._event_handlers[message].append(handler)

    def _handle_message(self, message: AbstractMessage, /) -> None:
        """Handle message.

        Args:
            message: Message to handle.

        """
        if not isinstance(message, AbstractMessage):  # type: ignore
            expected = "expected type 'AbstractMessage'"
            actual = f"got {type(message)} instead"
            error = ", ".join([expected, actual])
            raise TypeError(error)

        if not isinstance(message, (BaseCommand, BaseEvent)):
            msg = f"{type(message)} was not a 'Command' or an 'Event'"
            raise TypeError(msg)

        if isinstance(message, BaseCommand):
            self._pass_message_to_command_handler(message, on_error=RAISE)

        if isinstance(message, BaseEvent):
            self._pass_message_to_event_handlers(message, on_error=IGNORE)

    def _pass_message_to_command_handler(
        self,
        message: AbstractMessage,
        /,
        on_error: Literal["ignore", "raise"] = RAISE,
    ) -> None:
        """Pass message to command handler.

        Args:
            message: Message to handle.
            on_error (optional): Strategy for handling errors. Default ``raise``.

        """
        if not isinstance(message, BaseCommand):  # type: ignore
            expected = "expected type 'BaseCommand'"
            actual = f"got {type(message)} instead"
            msg = ", ".join([expected, actual])
            raise TypeError(msg)

        try:
            handler = self._command_handlers[type(message)]
            log.debug("Handling '%s' with handler %s", message, handler)
            handler(message)

        except Exception as error:
            handle_error(message, error, on_error=on_error)

        self._collect_events()

    def _pass_message_to_event_handlers(
        self,
        message: AbstractMessage,
        /,
        on_error: Optional[Literal["ignore", "raise"]] = IGNORE,
    ) -> None:
        """Pass message to event handlers.

        Args:
            message: Message to handle.
            on_error (optional): Strategy for handling errors. Default ``ignore``.

        """
        if not isinstance(message, BaseEvent):  # type: ignore
            expected = "expected type 'BaseEvent'"
            actual = f"got {type(message)} instead"
            msg = ", ".join([expected, actual])
            raise TypeError(msg)

        for handler in self._event_handlers[type(message)]:
            try:
                log.debug("Handling '%s' with handler %s", message, handler)
                handler(message)

            except Exception as error:
                handle_error(message, error, on_error=on_error)

            self._collect_events()

    def _collect_events(self) -> None:
        """Collect events."""
        if hasattr(self.uow, "collect_events"):
            events = list(eventcollector(self.uow))
            self.queue.extend(events)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def handle_error(
    message: AbstractMessage,
    error: Exception,
    *,
    on_error: Optional[Literal["ignore", "raise"]],
) -> None:
    """Handle error raised when handling message.

    Args:
        message: Message.
        error: Error raised when handling message.
        on_error: Strategy for handling errors.

    """
    exc_info = not config.is_production_environment()
    log.error("Error handling %s", message, exc_info=exc_info)
    if on_error == RAISE:
        raise error
