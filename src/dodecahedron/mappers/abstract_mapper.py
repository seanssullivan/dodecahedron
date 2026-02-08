# -*- coding: utf-8 -*-
"""Abstract Mapper."""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Mapping

__all__ = ["AbstractMapper"]


class AbstractMapper(abc.ABC):
    """Represents an abstract mapper."""

    @property
    @abc.abstractmethod
    def schema(self) -> Mapping[Hashable, Any]:
        """Mapped schema."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def properties(self) -> Dict[Hashable, Any]:
        """Mapped properties."""
        raise NotImplementedError
