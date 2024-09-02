# -*- coding: utf-8 -*-
"""Progressive Unit of Work."""

# Standard Library Imports
from __future__ import annotations

# Local Imports
from .abstract_unit_of_work import AbstractUnitOfWork
from ..progress import AbstractProgressBar

__all__ = ["ProgressiveUnitOfWork"]


class ProgressiveUnitOfWork(AbstractUnitOfWork):
    """Class implements a progressive unit of work.

    Args:
        *args (optional): Positional arguments.
        progress_bar: Progress bar.
        **kwargs (optional): Keyword arguments.

    Attributes:
        progress_bar: Progress bar.

    Raises:
        TypeError: when `progress_bar` parameter is not type 'tqdm'.

    """

    def __init__(
        self,
        *args,
        progress_bar: AbstractProgressBar,
        **kwargs,
    ) -> None:
        if not isinstance(progress_bar, AbstractProgressBar):
            expected = "expected type 'ProgressBar'"
            actual = f"got {type(progress_bar)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(*args, **kwargs)
        self._progress_bar = progress_bar

    def __exit__(self, *args) -> None:
        super().__exit__(*args)

        if self._progress_bar.leave is False:
            self._progress_bar.close()

    @property
    def progress(self) -> AbstractProgressBar:
        """Progress bar."""
        return self._progress_bar
