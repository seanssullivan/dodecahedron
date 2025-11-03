# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime
import time
from typing import Type

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.messages import BaseCommand
from dodecahedron.messages import BaseEvent
from dodecahedron.messages import AbstractMessage


@pytest.mark.parametrize("message", [AbstractMessage, BaseCommand, BaseEvent])
def test_sets_created_at_attribute(message: Type[AbstractMessage]) -> None:
    instance = message()
    result = getattr(instance, "__created_at__", None)
    assert result is not None
    assert isinstance(result, datetime.datetime)


@pytest.mark.parametrize("message", [AbstractMessage, BaseCommand, BaseEvent])
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
