# -*- coding: utf-8 -*-
"""String Converter.

Module provides function for converting values to strings.

"""

# Standard Library Imports
from typing import Optional

__all__ = ["to_string"]


def to_string(
    __value: object, /, default: Optional[str] = None
) -> Optional[str]:
    """Convert value to string.

    Args:
        value: Value to convert.

    Returns:
        String.

    """
    result = (
        str(__value)
        if __value is not None and not is_empty(__value)
        else default
    )
    return result


def is_empty(__value: object, /) -> bool:
    """Check whether value is empty.

    Args:
        __value: Value to check.

    Returns:
        Whether value is empty.

    """
    result = __value == ""
    return result
