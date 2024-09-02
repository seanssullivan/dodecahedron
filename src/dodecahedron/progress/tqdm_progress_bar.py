# -*- coding: utf-8 -*-
"""Tqdm Progress Bar."""

# Standard Library Imports
from typing import Optional
from typing import Union

# Third-Party Imports
from tqdm import tqdm

# Local Imports
from .abstract_progress_bar import AbstractProgressBar

__all__ = ["TqdmProgressBar"]


class TqdmProgressBar(AbstractProgressBar):
    """Implements a tqdm progress bar."""

    def __init__(
        self,
        desc: Optional[str] = None,
        total: Optional[Union[float, int]] = None,
        leave: bool = False,
        miniters: Union[float, int] = 1,
        **kwargs,
    ) -> None:
        self._progress_bar = tqdm(
            desc=desc,
            total=total,
            leave=leave,
            miniters=miniters,
            **kwargs,
        )

    @property
    def current(self) -> int:
        """Current progress."""
        return self._progress_bar.n

    @property
    def leave(self) -> bool:
        """Whether progress bar is maintained between iterations."""
        return self._progress_bar.leave

    @leave.setter
    def leave(self, value: bool) -> None:
        if not isinstance(value, bool):
            message = f"expected type 'bool', got {type(value)} instead"
            raise TypeError(message)

        self._progress_bar.leave = value

    @property
    def total(self) -> int:
        """Total progress."""
        return self._progress_bar.total

    @total.setter
    def total(self, n: Union[float, int]) -> None:
        if not isinstance(n, (float, int)):
            expected = "expected type 'float' or 'int'"
            actual = f"got {n} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._progress_bar.total = n

    def close(self) -> None:
        """Close progress bar."""
        self._progress_bar.close()

    def refresh(self) -> None:
        """Refresh progress bar."""
        self._progress_bar.refresh()

    def reset(self, total: Optional[Union[float, int]] = None) -> None:
        """Reset progress bar."""
        self._progress_bar.reset(total)

    def update(self, n: Union[float, int] = 1) -> None:
        """Update progress bar.

        Args:
            n (optional): Amount by which to increment the internal counter. Defaul ``1``.

        """
        self._progress_bar.update(n)

    def write(self, message: str) -> None:
        """Write message to progress bar."""
        self._progress_bar.write(message)
