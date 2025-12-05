# -*- coding: utf-8 -*-

__all__ = ["raise_for_instance"]


def raise_for_instance(__obj: object, __class: type) -> None:
    """Raise error when object is not instance of provided class.

    Args:
        __obj: Object for which to check class.
        __class: Class for which to check.

    Raises:
        TypeError: when object is not an instance of class.

    """
    if not isinstance(__obj, __class):
        expected = f"expected type '{__class.__name__!s}'"
        actual = f"got {type(__obj)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)
