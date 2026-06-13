# -*- coding: utf-8 -*-

# pylint: disable=too-few-public-methods

# Standard Library Imports
from datetime import datetime
from typing import Any
from typing import Optional

# Local Imports
from .abstract_models import AbstractModel
from .. import errors

__all__ = [
    "ContextMixin",
    "ParentMixin",
    "TrackingMixin",
]


class ContextMixin:
    """Mixin class for adding context to models.

    Args:
        *args (optional): Positional arguments.
        *kargs (optional): Keyword arguments.

    Attributes:
        context: Context of object.

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._context: Any = None

    @property
    def context(self) -> Any:
        """Context of object."""
        return self._context

    @context.deleter
    def context(self) -> None:
        self._context = None

    @context.setter
    def context(self, obj: Any) -> None:
        self._context = obj


class ParentMixin:
    """Mixin class for adding parent to models.

    Args:
        *args (optional): Positional arguments.
        *kargs (optional): Keyword arguments.

    Attributes:
        parent: Parent of object.

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._parent: Optional["AbstractModel"] = None

    @property
    def parent(self) -> Optional["AbstractModel"]:
        """Parent."""
        return self._parent

    @parent.setter
    def parent(self, obj: Any) -> None:
        errors.raise_for_instance(obj, AbstractModel)
        self._parent = obj


class TrackingMixin:
    """Mixin class for adding tracking attributes to models.

    Args:
        *args (optional): Positional arguments.
        created_at (optional): Datetime when object created. Default ``datetime.now()``.
        *kargs (optional): Keyword arguments.

    Attributes:
        is_removed: Whether object is removed.
        created_at: Datetime when object created.
        removed_at: Datetime when object removed.
        updated_at: Datetime when object updated.

    """

    def __init__(
        self,
        *args: Any,
        created_at: Optional[datetime] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._created_at = created_at or datetime.now()
        self._removed_at = None
        self._updated_at = None

    @property
    def created_at(self) -> datetime:
        """When object was created."""
        return getattr(self, "_created_at")

    @property
    def is_removed(self) -> bool:
        """Whether object is removed."""
        return self.removed_at is not None

    @property
    def removed_at(self) -> Optional[datetime]:
        """Datetime when object was removed."""
        return getattr(self, "_removed_at", None)

    @removed_at.deleter
    def removed_at(self) -> None:
        setattr(self, "_removed_at", None)

    @removed_at.setter
    def removed_at(self, value: object) -> None:
        errors.raise_for_instance(value, datetime)
        setattr(self, "_removed_at", value)

    @property
    def updated_at(self) -> Optional[datetime]:
        """Datetime when object was updated."""
        return getattr(self, "_updated_at", None)

    @updated_at.deleter
    def updated_at(self) -> None:
        setattr(self, "_updated_at", None)

    @updated_at.setter
    def updated_at(self, value: object) -> None:
        errors.raise_for_instance(value, datetime)
        setattr(self, "_updated_at", value)
