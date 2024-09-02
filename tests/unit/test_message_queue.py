# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.messages import BaseMessage
from dodecahedron.queue import MessageQueue
from .. import factories


def test_instantiates_message_queue_without_arguments() -> None:
    """Tests that an empty message queue can be instantiated."""
    result = MessageQueue()
    assert isinstance(result, MessageQueue)


def test_instantiates_message_queue_with_iterable() -> None:
    """Tests that a queue can be instantiated with messages."""
    result = MessageQueue(factories.make_messages(3))
    assert isinstance(result, MessageQueue)


def test_raises_error_when_argument_not_iterable() -> None:
    """Tests that an error is raised when argument is not iterable."""
    with pytest.raises(TypeError):
        MessageQueue(1)


def test_raises_error_when_argument_not_messages() -> None:
    """Tests that an error is raised when passed invalid arguments."""
    with pytest.raises(TypeError):
        MessageQueue([1, 2, 3])


def test_sorts_messages_when_instantiated() -> None:
    """Tests that messages are always sorted after instantiation."""
    message1, message2, message3 = factories.make_messages(3, delay=1e-6)

    queue = MessageQueue([message3, message2, message1])
    assert list(queue) == [message1, message2, message3]


def test_returns_length_of_queue() -> None:
    """Tests that `len()` returns the number of messages."""
    queue = MessageQueue(factories.make_messages(3))
    assert len(queue) == 3


def test_returns_next_message_in_queue() -> None:
    """Tests that `next()` returns the next message in queue."""
    message1, message2, message3 = factories.make_messages(3)
    queue = MessageQueue([message1, message2, message3])
    assert next(queue) == message1


def test_raises_error_when_empty() -> None:
    """Tests that `next()` raises an error when queue is empty."""
    queue = MessageQueue()

    with pytest.raises(StopIteration):
        next(queue)


def test_appends_to_queue() -> None:
    """Tests that a message can be appended to the queue."""
    queue = MessageQueue(factories.make_messages(3))
    assert len(queue) == 3

    queue.append(BaseMessage())
    assert len(queue) == 4


def test_sorts_queue_after_appending_message() -> None:
    """Tests that the queue remains sorted after appending a message."""
    message1, message2, message3 = factories.make_messages(3)
    queue = MessageQueue([message2, message3])
    queue.append(message1)
    assert list(queue) == [message1, message2, message3]


def test_extends_queue() -> None:
    """Tests that the queue can be extended with new messages."""
    queue = MessageQueue([BaseMessage()])
    assert len(queue) == 1

    queue.extend([BaseMessage(), BaseMessage()])
    assert len(queue) == 3


def test_sorts_queue_after_extending() -> None:
    """Tests that the queue remains sorted after it is extended."""
    message1, message2, message3 = factories.make_messages(3, delay=1e-6)

    queue = MessageQueue([message3])
    queue.extend([message2, message1])
    assert list(queue) == [message1, message2, message3]


def test_returns_true_when_queue_contains_messages() -> None:
    """Tests that queues containing messages are truthy."""
    result = MessageQueue(factories.make_messages(3))
    assert result


def test_returns_false_when_queue_is_empty() -> None:
    """Tests that queues without messages are falsy."""
    result = MessageQueue()
    assert not result


def test_loops_over_queue_until_empty() -> None:
    """Tests that message queue can used in a while loop."""
    queue = MessageQueue(factories.make_messages(3))

    count = 0
    while queue:
        queue.popleft()
        count += 1

    assert not queue
    assert count == 3


def test_clears_queue() -> None:
    """Tests that `clear()` method empties a message queue."""
    queue = MessageQueue(factories.make_messages(3))
    assert len(queue) == 3

    queue.clear()
    assert len(queue) == 0
