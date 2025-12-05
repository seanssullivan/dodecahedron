# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import time
from typing import List
from typing import Union

# Local Imports
from dodecahedron import messages


def make_commands(
    n: int, *, delay: Union[float, int] = 0
) -> List[messages.AbstractCommand]:
    """Make commands.

    Args:
        n: Number of commands.
        delay (optional): Delay before instantiating command. Default ``0``.

    Returns:
        Commands.

    """
    results = [make_event(delay=delay) for _ in range(n)]
    return results


def make_commands(*, delay: Union[float, int] = 0) -> messages.AbstractCommand:
    """Make commands.

    Args:
        delay (optional): Delay before instantiating commands. Default ``0``.

    Returns:
        Commands.

    Raises:
        TypeError: when `delay` is not type ``float`` or ``int``.

    """
    if not isinstance(delay, (float, int)):
        message = f"expected type 'float' or 'int', got {type(delay)} instead"
        raise TypeError(message)

    time.sleep(delay)
    result = messages.AbstractEvent()
    return result


def make_events(
    n: int, *, delay: Union[float, int] = 0
) -> List[messages.AbstractEvent]:
    """Make events.

    Args:
        n: Number of events.
        delay (optional): Delay before instantiating event. Default ``0``.

    Returns:
        Events.

    """
    results = [make_event(delay=delay) for _ in range(n)]
    return results


def make_event(*, delay: Union[float, int] = 0) -> messages.AbstractEvent:
    """Make event.

    Args:
        delay (optional): Delay before instantiating event. Default ``0``.

    Returns:
        Event.

    Raises:
        TypeError: when `delay` is not type ``float`` or ``int``.

    """
    if not isinstance(delay, (float, int)):
        message = f"expected type 'float' or 'int', got {type(delay)} instead"
        raise TypeError(message)

    time.sleep(delay)
    result = messages.AbstractEvent()
    return result


def make_messages(
    n: int, *, delay: Union[float, int] = 0
) -> List[messages.AbstractMessage]:
    """Make messages.

    Args:
        n: Number of messages.
        delay (optional): Delay before instantiating message. Default ``0``.

    Returns:
        Message.

    """
    results = [make_message(delay=delay) for _ in range(n)]
    return results


def make_message(*, delay: Union[float, int] = 0) -> messages.AbstractMessage:
    """Make message.

    Args:
        delay (optional): Delay before instantiating message. Default ``0``.

    Returns:
        Message.

    Raises:
        TypeError: when `delay` is not type ``float`` or ``int``.

    """
    if not isinstance(delay, (float, int)):
        message = f"expected type 'float' or 'int', got {type(delay)} instead"
        raise TypeError(message)

    time.sleep(delay)
    result = messages.AbstractMessage()
    return result
