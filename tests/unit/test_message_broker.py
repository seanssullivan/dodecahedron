# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from unittest import mock

# Local Imports
from dodecahedron.messagebroker import BaseMessageBroker


def test_instantiates_message_broker() -> None:
    """Tests that message broker can be instantiated."""
    result = BaseMessageBroker()
    assert isinstance(result, BaseMessageBroker)


def test_message_broker_is_singleton() -> None:
    broker1 = BaseMessageBroker()
    broker2 = BaseMessageBroker()
    assert broker1 is broker2


def test_message_broker_maintains_subscribers() -> None:
    subscriber = mock.Mock()

    broker1 = BaseMessageBroker()
    broker1.subscribe("test", subscriber)

    broker2 = BaseMessageBroker()
    results = broker2.subscribers["test"]
    assert subscriber in results
