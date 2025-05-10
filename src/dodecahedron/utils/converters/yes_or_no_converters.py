# -*- coding: utf-8 -*-
"""Yes or No Converter.

Module provides function for converting values to 'Yes' or 'No'.

"""

# Standard Library Imports
from typing import Literal
from typing import Optional

# Local Imports
from .boolean_converter import BooleanConverter

__all__ = ["to_y_or_n", "to_yes_or_no"]


def to_y_or_n(
    __value: object, /, default: Optional[str] = None
) -> Optional[Literal["Y", "N"]]:
    """Convert value to `Y` or `N`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Y` or `N`.

    """
    if default and default not in ("Y", "N"):
        message = f"expected value of 'Y' or 'N', got {default} instead"
        raise ValueError(message)

    try:
        converter = BooleanConverter()
        value = converter(__value) if __value else default

    except TypeError:
        message = f"{type(__value)} cannot be converted to 'Y' or 'N'"
        raise TypeError(message)

    except ValueError:
        message = f"'{__value}' cannot be converted to 'Y' or 'N'"
        raise ValueError(message)

    result = "Y" if value is True else "N"
    return result


def to_yes_or_no(
    __value: object, /, default: Optional[str] = None
) -> Optional[Literal["Yes", "No"]]:
    """Convert value to `Yes` or `No`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Yes` or `No`.

    """
    if default and default not in ("Yes", "No"):
        message = f"expected value of 'Yes' or 'No', got {default} instead"
        raise ValueError(message)

    try:
        converter = BooleanConverter()
        value = converter(__value) if __value else default

    except TypeError as error:
        message = f"{type(__value)} cannot be converted to 'Yes' or 'No'"
        raise TypeError(message) from error

    except ValueError as error:
        message = f"'{__value}' cannot be converted to 'Yes' or 'No'"
        raise ValueError(message) from error

    result = "Yes" if value is True else "No"
    return result
