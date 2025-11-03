# -*- coding: utf-8 -*-
"""Progressive Dispatcherr."""

# Local Imports
from .base_dispatcher import BaseDispatcher
from ..messagebus import AbstractMessageBus
from ..progress import AbstractProgressBar
from ..units_of_work import ProgressiveUnitOfWork

__all__ = ["ProgressiveDispatcher"]


class ProgressiveDispatcher(BaseDispatcher):
    """Implements a progressive dispatcher.

    Args:
        __bus: Message bus.

    Attributes:
        messagebus: Message bus.
        progress: Progress bar.

    """

    def __init__(self, __bus: AbstractMessageBus, /) -> None:
        if not isinstance(__bus.uow, ProgressiveUnitOfWork):
            expected = "expected type 'ProgressiveUnitOfWork'"
            actual = f"got {type(__bus.uow)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(__bus)

    @property
    def progress(self) -> AbstractProgressBar:
        """Progress bar."""
        result = getattr(self.messagebus.uow, "progress")
        return result
