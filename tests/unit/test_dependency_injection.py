# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import Dict

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.messages import AbstractCommand
from dodecahedron.messages import AbstractEvent
from dodecahedron.messages import AbstractMessage
from dodecahedron.handlers import CommandHandlers
from dodecahedron.handlers import EventHandlers
from dodecahedron.handlers import inject_handler_dependencies


class TestCommand(AbstractCommand): ...


class TestEvent(AbstractEvent): ...


def test_injects_command_handler_dependency() -> None:
    """Tests that dependency is injected into command handler."""

    def test_handler(dep: Any) -> None:
        assert dep is not None

    handlers: CommandHandlers = {TestCommand: test_handler}
    dependencies: Dict[str, Any] = {"dep": True}
    results = inject_handler_dependencies(handlers, dependencies)
    results[TestCommand]()


def test_injects_event_handler_dependency() -> None:
    """Tests that dependency is injected into event handler."""

    def test_handler(dep: Any) -> None:
        assert dep is not None

    handlers: EventHandlers = {TestEvent: [test_handler]}
    dependencies: Dict[str, Any] = {"dep": True}
    results = inject_handler_dependencies(handlers, dependencies)
    results[TestEvent][0]()


def test_raises_error_when_argument_is_neither_command_nor_event() -> None:
    """Tests that function raises error."""

    class TestError(AbstractMessage): ...

    def test_handler(dep: Any) -> None:
        assert dep is not None

    handlers = {TestError: test_handler}
    dependencies: Dict[str, Any] = {"dep": True}

    with pytest.raises(NotImplementedError):
        inject_handler_dependencies(handlers, dependencies)  # type: ignore
