# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Callable
from unittest import mock

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.messages import AbstractCommand
from dodecahedron.messages import AbstractEvent
from dodecahedron.messagebus import MessageBus
from dodecahedron.units_of_work import EventfulUnitOfWork


class TestCommand(AbstractCommand): ...


class TestEvent(AbstractEvent): ...


def test_instantiates_messagebus() -> None:
    """Tests that messagebus can be instantiated."""
    uow = EventfulUnitOfWork()
    result = MessageBus(uow, {}, {})
    assert isinstance(result, MessageBus)


def test_passes_command_to_command_handler() -> None:
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {TestCommand: handler}, {})  # type: ignore
    bus.handle(TestCommand())
    handler.assert_called()


def test_does_not_pass_command_to_event_handler() -> None:
    command_handler: Callable[..., None] = mock.Mock()
    event_handler: Callable[..., None] = mock.Mock()

    command_handlers = {TestCommand: command_handler}
    event_handlers = {TestEvent: [event_handler]}

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, command_handlers, event_handlers)  # type: ignore
    bus.handle(TestCommand())
    event_handler.assert_not_called()


def test_raises_error_from_command_handler() -> None:
    class TestError(Exception): ...

    def test_handler(*_) -> None:
        raise TestError()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {TestCommand: test_handler}, {})  # type: ignore

    with pytest.raises(TestError):
        bus.handle(TestCommand())


def test_executes_callback_after_passing_command_to_handler() -> None:
    callback: Callable[..., None] = mock.Mock()
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {TestCommand: handler}, {})  # type: ignore
    bus.handle(TestCommand(), callback=callback)
    callback.assert_called()


def test_passes_event_to_event_handler() -> None:
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {}, {TestEvent: [handler]})  # type: ignore
    bus.handle(TestEvent())
    handler.assert_called()


def test_does_not_pass_event_to_command_handler() -> None:
    command_handler: Callable[..., None] = mock.Mock()
    event_handler: Callable[..., None] = mock.Mock()

    command_handlers = {TestCommand: command_handler}
    event_handlers = {TestEvent: [event_handler]}

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, command_handlers, event_handlers)  # type: ignore
    bus.handle(TestEvent())
    command_handler.assert_not_called()


def test_does_not_raise_error_from_event_handler() -> None:
    class TestError(Exception): ...

    def test_handler(*_) -> None:
        raise TestError()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {}, {TestEvent: [test_handler]})  # type: ignore
    bus.handle(TestEvent())


def test_executes_callback_after_passing_event_to_handler() -> None:
    callback: Callable[..., None] = mock.Mock()
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {}, {TestEvent: [handler]})  # type: ignore
    bus.handle(TestEvent(), callback=callback)
    callback.assert_called()


def test_subscribes_handler_to_command() -> None:
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {}, {})  # type: ignore
    bus.subscribe(TestCommand, handler)
    bus.handle(TestCommand())
    handler.assert_called()


def test_subscribes_handler_to_event() -> None:
    handler: Callable[..., None] = mock.Mock()

    uow = EventfulUnitOfWork()
    bus = MessageBus(uow, {}, {})  # type: ignore
    bus.subscribe(TestEvent, handler)
    bus.handle(TestEvent())
    handler.assert_called()
