# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
import functools
from types import FunctionType
from types import MethodType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
import warnings

__all__ = ["TrackerMeta"]


# Constants
ADD_METHOD = "add"
GET_METHOD = "get"
LIST_METHOD = "list"
REMOVE_METHOD = "remove"
SEEN_ATTR = "__seen__"

# Custom types
T = TypeVar("T")


class TrackerMeta(abc.ABCMeta):
    """Metaclass for tracking child objects."""

    def __new__(
        meta,  # type: ignore
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwargs: Any,
    ) -> type:
        wrapped_attrs = meta.wrap_attributes(namespace)
        return super().__new__(meta, name, bases, wrapped_attrs, **kwargs)

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, SEEN_ATTR, set())
        return instance

    @classmethod
    def wrap_attributes(cls, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Wrap attributes.

         Args:
            attrs: Attributes to wrap.

        Returns:
            Wrapped attributes.

        """
        results = {
            key: (
                cls.wrap_method(key, value)
                if isinstance(value, (FunctionType, MethodType))
                else value
            )
            for key, value in attrs.items()
        }
        return results

    @classmethod
    def wrap_method(cls, name: str, method: Any) -> Callable[..., Any]:
        """Wrap method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """
        if not isinstance(method, (FunctionType, MethodType)):
            message = f"expected method, got type {type(method)} instead"
            raise TypeError(message)

        if name == ADD_METHOD:
            return track_first_positional_argument(method)

        if name == GET_METHOD:
            return track_single_return_value(method)

        if name == LIST_METHOD:
            return track_multiple_return_values(method)

        if name == REMOVE_METHOD:
            return track_first_positional_argument(method)

        return method


def track_first_positional_argument(
    method: Callable[..., Any], /
) -> Callable[..., Any]:
    """Track first positional argument passed to method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    Raises:
        TypeError: when argument is not a method.

    """
    if not isinstance(method, (FunctionType, MethodType)):
        message = f"expected method, got type {type(method)} instead"
        raise TypeError(message)

    @functools.wraps(method)
    def wrapper(self: Any, obj: object, /, *args: Any, **kwargs: Any) -> Any:
        """Wrapper applied to decorated method.

        Args:
            obj: Object to track.
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        result = method(self, obj, *args, **kwargs)

        # We only add objects to those seen after the method executes
        # successfully. We don't want to track objects that raise exceptions.
        add_seen_object(self, obj)
        return result

    functools.update_wrapper(wrapper, method)
    return wrapper


def track_multiple_return_values(
    method: Callable[..., Any], /
) -> Callable[..., Any]:
    """Track all values returned from method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    Raises:
        TypeError: when argument is not a method.

    """
    if not isinstance(method, (FunctionType, MethodType)):
        message = f"expected method, got type {type(method)} instead"
        raise TypeError(message)

    @functools.wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Sequence[Any]:
        """Wrapper applied to decorated method.

        Args:
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Results of called method.

        """
        results = method(self, *args, **kwargs)
        if results is not None:
            update_seen_objects(self, results)

        return results

    functools.update_wrapper(wrapper, method)
    return wrapper


def track_single_return_value(
    method: Callable[..., Any], /
) -> Callable[..., Any]:
    """Track each value returned from method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    Raises:
        TypeError: when argument is not a method.

    """
    if not isinstance(method, (FunctionType, MethodType)):
        message = f"expected method, got type {type(method)} instead"
        raise TypeError(message)

    @functools.wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Wrapper applied to decorated method.

        Args:
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        result = method(self, *args, **kwargs)
        if result is not None:
            add_seen_object(self, result)

        return result

    functools.update_wrapper(wrapper, method)
    return wrapper


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def add_seen_object(parent: Any, child: Any) -> None:
    """Add value to seen objects.

    Args:
        parent: Parent object.
        child: Child object seen.

    """
    try:
        set_default_attr(parent, SEEN_ATTR, set())
        seen: Set[Any] = getattr(parent, SEEN_ATTR)
        seen.add(child)

    except TypeError:
        message = "Tracking decorator does not support unhashable objects"
        warnings.warn(message)


def update_seen_objects(parent: Any, children: Sequence[Any]) -> None:
    """Add results to seen objects.

    Args:
        parent: Parent object.
        children: Child objects seen.

    """
    try:
        set_default_attr(parent, SEEN_ATTR, set())
        seen: Set[Any] = getattr(parent, SEEN_ATTR)
        seen.update(children)

    except TypeError:
        message = "Tracking decorator does not support unhashable objects"
        warnings.warn(message)


def set_default_attr(obj: object, attr: str, value: Any) -> None:
    """Set default value of attribute on object.

    Args:
        obj: Object on which to set default attribute.
        attr: Name of attribute to set.
        value: Value to which to set attribute.

    """
    if not hasattr(obj, attr):
        setattr(obj, attr, value)
