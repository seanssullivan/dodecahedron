# -*- coding: utf-8 -*-

# Standard Library Imports
import collections
import functools
import inspect
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import overload
from typing import Type
from typing import Union

# Local Imports
from .messages import AbstractCommand
from .messages import AbstractEvent

__all__ = [
    "inject_handler_dependencies",
    "inject_dependencies",
    "merge_event_handlers",
]


# Custom types
Handler = Callable[..., None]
CommandHandlers = Dict[Type[AbstractCommand], Handler]
EventHandlers = Dict[Type[AbstractEvent], List[Handler]]


@overload
def inject_handler_dependencies(
    __handlers: CommandHandlers,
    /,
    dependencies: Dict[str, Any],
) -> CommandHandlers: ...


@overload
def inject_handler_dependencies(
    __handlers: EventHandlers,
    /,
    dependencies: Dict[str, Any],
) -> EventHandlers: ...


def inject_handler_dependencies(
    __handlers: Union[CommandHandlers, EventHandlers],
    /,
    dependencies: Dict[str, Any],
) -> Union[CommandHandlers, EventHandlers]:
    """Inject dependencies into handlers.

    Args:
        __handlers: Message handlers.
        dependencies: Dependencies.

    Returns:
        Handlers.

    """
    if all(issubclass(key, AbstractCommand) for key in __handlers.keys()):
        results = inject_command_handler_dependencies(__handlers, dependencies)  # type: ignore

    elif all(issubclass(key, AbstractEvent) for key in __handlers.keys()):
        results = inject_event_handler_dependencies(__handlers, dependencies)  # type: ignore

    else:
        raise NotImplementedError

    return results


def inject_command_handler_dependencies(
    __handlers: CommandHandlers, /, dependencies: Dict[str, Any]
) -> CommandHandlers:
    """Inject dependencies into command handlers.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        __handlers: Command handlers.
        dependencies: Dependencies.

    Returns:
        Command handlers.

    Raises:
        TypeError: when `handlers` is not type 'dict'.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    if not isinstance(__handlers, dict):  # type: ignore
        message = f"expected type 'dict', got {type(__handlers)} instead"
        raise TypeError(message)

    results = {
        command_type: inject_dependencies(command_handler, dependencies)
        for command_type, command_handler in __handlers.items()
    }
    return results


def inject_event_handler_dependencies(
    __handlers: EventHandlers, /, dependencies: Dict[str, Any]
) -> EventHandlers:
    """Inject dependencies into event handlers.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        __handlers: Event handlers.
        dependencies: Dependencies.

    Returns:
        Event handlers.

    Raises:
        TypeError: when `handlers` is not type 'dict'.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    if not isinstance(__handlers, dict):  # type: ignore
        message = f"expected type 'dict', got {type(__handlers)} instead"
        raise TypeError(message)

    results = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in __handlers.items()
    }
    return results


def inject_dependencies(
    __handler: Handler,
    /,
    dependencies: Dict[str, Any],
) -> Handler:
    """Inject dependencies into handler function.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        __handler: Handler function.
        dependencies: Dependencies.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    params = inspect.signature(__handler).parameters
    kwargs = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    result = functools.partial(__handler, **kwargs)
    return result


def merge_event_handlers(*args: EventHandlers) -> EventHandlers:
    """Merge event handlers.

    Args:
        *args: Groups of event handlers.

    Returns:
        Merged event handlers.

    """
    collection: EventHandlers = collections.defaultdict(list)
    for arg in args:
        for event_type, handlers in arg.items():
            collection[event_type].extend(handlers)

    result = dict(collection)
    return result
