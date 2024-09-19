# -*- coding: utf-8 -*-
"""Distance Converter.

Module provides functions for converting values to distances.

"""

# Standard Library Imports
import decimal
import re
import typing

# Local Imports
from .base_converter import BaseConverter

__all__ = ["to_distance"]


def to_distance(__value: typing.Any, /, default: float = 0.0) -> float:
    """Convert value to distance.

    Args:
        __value: Value to convert to distance.
        default (optional): Default value. Default ``0.0``.

    Returns:
        Distance.

    """
    converter = DistanceConverter(default=default)
    result = converter(__value)
    return result


class DistanceConverter(BaseConverter):
    """Class implements a distance converter.

    Args:
        default (optional): Default value. Default ``0.0``.
        on_error (optional): Whether to raise error or return default. Default ``raise``.

    """

    def __init__(
        self,
        *,
        default: float = 0.0,
        on_error: typing.Literal["default", "raise"] = "raise",
    ) -> None:
        if not isinstance(default, float):
            message = f"expected type 'float', got {type(default)} instead"
            raise TypeError(message)

        super().__init__(default=default, on_error=on_error)
        self._conversions.update(DEFAULT_CONVERSIONS)
        self._conversions = self._conversions.new_child()


def distance_from_decimal(__value: decimal.Decimal, _: float, /) -> float:
    """Convert decimal value to distance.

    Args:
        __value: Value to convert to distance.

    Returns:
        Distance.

    Raises:
        TypeError: when value is not type 'Decimal'.

    """
    if not isinstance(__value, decimal.Decimal):
        message = f"expected type 'Decimal', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def distance_from_float(__value: float, _: float, /) -> float:
    """Convert float value to distance.

    Args:
        __value: Value to convert to distance.

    Returns:
        Distance.

    Raises:
        TypeError: when value is not type 'float'.

    """
    if not isinstance(__value, float):
        message = f"expected type 'float', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def distance_from_int(__value: int, _: float, /) -> float:
    """Convert integer value to distance.

    Args:
        __value: Value to convert to distance.

    Returns:
        Distance.

    Raises:
        TypeError: when value is not type 'int'.

    """
    if not isinstance(__value, int):
        message = f"expected type 'int', got {type(__value)} instead"
        raise TypeError(message)

    result = float(__value)
    return result


def distance_from_str(__value: str, default: float = 0.0, /) -> float:
    """Convert string value to distance.

    Args:
        __value: String representation of distance value.

    Returns:
        Distance.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to distance.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        representation = re.sub(r"[^0-9a-zA-Z.]+", r"", value)
        number = re.sub(r"(\d+)\s?m?", r"\1", representation, flags=re.I)
        result = float(number)

    except ValueError:
        message = f"{type(__value)} cannot be converted to distance"
        raise ValueError(message)

    else:
        return result


DEFAULT_CONVERSIONS = {
    decimal.Decimal: distance_from_decimal,
    float: distance_from_float,
    int: distance_from_int,
    str: distance_from_str,
}  # type: typing.Dict[type, typing.Callable]
