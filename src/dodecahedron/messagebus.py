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
import functools
import logging
from operator import methodcaller
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

# Local Imports
from .errors import BaseError
from .messages import BaseCommand
from .messages import BaseEvent
from .messages import BaseMessage
from .queue import MessageQueue
from .units_of_work import AbstractUnitOfWork

__all__ = ["BaseMessageBus"]


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Constants
eventcollector = methodcaller("collect_events")


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
    def queue(self) -> MessageQueue[BaseMessage]:
        """Message queue."""
        raise NotImplementedError

    @abc.abstractmethod
    def handle(self, message: BaseMessage) -> None:
        """Handle a message.

        Args:
            message: Message to handle.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(self, message: Type[BaseMessage], handler: Callable) -> None:
        """Subscribe a handler for a `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.

        """
        raise NotImplementedError


class BaseMessageBus(AbstractMessageBus):
    """Implements a base class for message buses to inherit.

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
        command_handlers: Dict[Type[BaseCommand], Callable],
        event_handlers: Dict[Type[BaseEvent], List[Callable]],
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
    def queue(self) -> MessageQueue[BaseMessage]:
        """Message queue."""
        return self._queue

    def handle(self, message: BaseMessage) -> None:
        """Handle a message.

        Provided message is passed to an appropriate handler function.

        Args:
            message: Message.

        """
        self.queue.append(message)
        while self.queue:
            message = self.queue.popleft()
            self.handle_message(message)

    def subscribe(self, message: Type[BaseMessage], handler: Callable) -> None:
        """Subscribe a handler for a `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.
            handler: Handler function to subscribe.

        """
        if issubclass(message, BaseCommand):
            self._command_handlers[message] = handler
        elif issubclass(message, BaseEvent):
            self._event_handlers[message].append(handler)
        else:
            error = f"{type(message)} is not a 'Command' or an 'Event'"
            raise TypeError(error)

    def handle_message(self, message: BaseMessage) -> None:
        """Handle message.

        Args:
            message: Message to handle.

        """
        if isinstance(message, BaseCommand):
            self.handle_command(message)
        elif isinstance(message, BaseEvent):
            self.handle_event(message)
        else:
            error = f"{message} was not a 'Command' or an 'Event'"
            raise TypeError(error)

    def handle_command(self, command: BaseCommand) -> None:
        """Handle command.

        Args:
            command: Command to handle.

        """
        try:
            handler = self._command_handlers[type(command)]
            handler(command)
        except BaseError as error:
            log.exception("Error handlings %s", command)
            raise error
        else:
            self.collect_events()

    def handle_event(self, event: BaseEvent) -> None:
        """Handle event.

        Args:
            event: Event to handle.

        """
        for handler in self._event_handlers[type(event)]:
            try:
                log.debug("handling event %s with handler %s", event, handler)
                handler(event)
            except BaseError:
                log.exception("Error handling %s", event)
            else:
                self.collect_events()

    def collect_events(self) -> None:
        """Collect events."""
        if hasattr(self.uow, "collect_events"):
            events = list(eventcollector(self.uow))
            self.queue.extend(events)
