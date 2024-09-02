# -*- coding: utf-8 -*-
"""File Mode Converters."""

# Standard Library Imports
import re

__all__ = [
    "to_bytes_file_mode",
    "to_text_file_mode",
]


def to_bytes_file_mode(mode: str) -> str:
    """Convert to bytes file mode.

    Args:
        mode: Mode.

    Returns:
        Mode.

    """
    result = re.sub(r"[bt]?([arw])[bt]?", r"\g<1>b", mode)
    return result


def to_text_file_mode(mode: str) -> str:
    """Convert to text file mode.

    Args:
        mode: Mode.

    Returns:
        Mode.

    """
    result = re.sub(r"[bt]?([arw])[bt]?", r"\g<1>t", mode)
    return result
