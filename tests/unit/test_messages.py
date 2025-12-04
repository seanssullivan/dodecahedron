# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime
from dataclasses import dataclass
import time
from typing import Type

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.messages import AbstractCommand
from dodecahedron.messages import AbstractEvent
from dodecahedron.messages import AbstractMessage


@pytest.mark.parametrize(
    "message", [AbstractMessage, AbstractCommand, AbstractEvent]
)
def test_sets_created_at_attribute(message: Type[AbstractMessage]) -> None:
    instance = message()
    result = getattr(instance, "__created_at__", None)
    assert result is not None
    assert isinstance(result, datetime.datetime)


@pytest.mark.parametrize(
    "message", [AbstractMessage, AbstractCommand, AbstractEvent]
)
def test_sorts_messages_in_order_created(
    message: Type[AbstractMessage],
) -> None:
    message1 = message()
    time.sleep(1e-6)
    message2 = message()
    time.sleep(1e-6)
    message3 = message()

    expected = [message1, message2, message3]
    result = sorted([message3, message2, message1])
    assert result == expected


@pytest.mark.parametrize(
    "message", [AbstractMessage, AbstractCommand, AbstractEvent]
)
def test_dataclasses_are_subclasses_of_parent_message_class(
    message: Type[AbstractMessage],
) -> None:
    @dataclass
    class TestMessage(message): ...

    assert isinstance(TestMessage(), message)
