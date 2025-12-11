# -*- coding: utf-8 -*-

# Standard Library Imports
import re

__all__ = ["parse_number"]


def parse_number(__value: str, /) -> float:
    """Parse number from string.

    Args:
        __value: String that contains a number.

    Returns:
        String representation of number.

    Raises:
        TypeError: when value is not type 'str'.

    """
    if not isinstance(__value, str):  # type: ignore  # pragma: no cover
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    representation = re.sub(r"[^0-9a-zA-Z.]+", r"", value)
    number = re.sub(r"(\d+)\s?[a-z]*", r"\1", representation, flags=re.I)
    result = float(number)
    return result
