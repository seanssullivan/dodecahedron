# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from unittest import mock

# Local Imports
from dodecahedron.messagebrokers import MessageBroker


def test_instantiates_message_broker() -> None:
    """Tests that message broker can be instantiated."""
    result = MessageBroker()
    assert isinstance(result, MessageBroker)


def test_message_broker_is_singleton() -> None:
    broker1 = MessageBroker()
    broker2 = MessageBroker()
    assert broker1 is broker2


def test_message_broker_maintains_subscribers() -> None:
    subscriber = mock.Mock()

    broker1 = MessageBroker()
    broker1.subscribe("test", subscriber)

    broker2 = MessageBroker()
    results = broker2.subscribers["test"]
    assert subscriber in results
