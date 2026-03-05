# -*- coding: utf-8 -*-
"""Abstract Mapper."""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List
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

    @abc.abstractmethod
    def from_dict(self, __dict: Dict[Hashable, Any], /) -> Any:
        """Instantiate object from dictionary.

        Args:
            __dict: Dictionary.

        Returns:
            Instance of object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def from_list(self, __list: List[Any], /) -> Any:
        """Instantiate object from list.

        Args:
            __list: List.

        Returns:
            Instance of object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self, __obj: Any, /) -> Dict[Hashable, Any]:
        """Convert object to dictionary.

        Args:
            __obj: Object.

        Returns:
            Dictionary.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, __obj: Any, /) -> List[Any]:
        """Convert object to list.

        Args:
            __obj: Object.

        Returns:
            List.

        """
        raise NotImplementedError
