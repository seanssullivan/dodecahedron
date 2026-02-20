# -*- coding: utf-8 -*-
"""Yes or No Converter.

Module provides function for converting values to 'Yes' or 'No'.

"""

# Standard Library Imports
from typing import Any
from typing import Literal
from typing import Optional
from typing import overload

# Local Imports
from .boolean_converter import BooleanConverter

__all__ = ["to_y_or_n", "to_yes_or_no"]


@overload
def to_y_or_n(
    __value: Any,
    /,
    default: Literal["Y", "N"],
) -> Literal["Y", "N"]: ...


@overload
def to_y_or_n(
    __value: Any,
    /,
    default: Optional[Literal["Y", "N"]] = None,
) -> Optional[Literal["Y", "N"]]: ...


def to_y_or_n(
    __value: Any,
    /,
    default: Optional[str] = "N",
) -> Optional[Literal["Y", "N"]]:
    """Convert value to `Y` or `N`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Y` or `N`.

    """
    if default is not None and default not in ("Y", "N"):
        message = f"expected value of 'Y' or 'N', got {default} instead"
        raise ValueError(message)

    try:
        converter = BooleanConverter()
        converter.default = converter(default) if default is not None else None
        value = converter(__value)

    except TypeError:
        message = f"{type(__value)} cannot be converted to 'Y' or 'N'"
        raise TypeError(message)

    except ValueError:
        message = f"'{__value}' cannot be converted to 'Y' or 'N'"
        raise ValueError(message)

    result: Optional[Literal["Y", "N"]] = (
        ("Y" if value is True else "N") if value is not None else None
    )
    return result


@overload
def to_yes_or_no(
    __value: Any,
    /,
    default: Literal["Yes", "No"],
) -> Literal["Yes", "No"]: ...


@overload
def to_yes_or_no(
    __value: Any,
    /,
    default: Optional[Literal["Yes", "No"]] = None,
) -> Optional[Literal["Yes", "No"]]: ...


def to_yes_or_no(
    __value: object,
    /,
    default: Optional[str] = "No",
) -> Optional[Literal["Yes", "No"]]:
    """Convert value to `Yes` or `No`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Yes` or `No`.

    """
    if default is not None and default not in ("Yes", "No"):
        message = f"expected value of 'Yes' or 'No', got {default} instead"
        raise ValueError(message)

    try:
        converter = BooleanConverter()
        converter.default = converter(default) if default is not None else None
        value = converter(__value)

    except TypeError as error:
        message = f"{type(__value)} cannot be converted to 'Yes' or 'No'"
        raise TypeError(message) from error

    except ValueError as error:
        message = f"'{__value}' cannot be converted to 'Yes' or 'No'"
        raise ValueError(message) from error

    result: Optional[Literal["Yes", "No"]] = (
        ("Yes" if value is True else "No") if value is not None else None
    )
    return result
