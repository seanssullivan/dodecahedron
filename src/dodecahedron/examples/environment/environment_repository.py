# -*- coding: utf-8 -*-

# Standard Library Imports
from datetime import datetime
import operator
import os
from typing import Any
from typing import List
from typing import Optional
from typing import Sequence

# Local Imports
from .variable_model import EnvironmentVariable
from ...repositories.abstract_repository import AbstractRepository
from ... import errors

__all__ = ["EnvironmentRepository"]


class EnvironmentRepository(AbstractRepository):
    """Class implements an environment variable repository.

    Args:
        *args (optional): Positional arguments.
        mapper (optional): Mapper. Default ``None``.
        **kwargs (optional): Keyword arguments.

    """

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._session = os.environ
        self.load()

        # Tracking attributes
        self._committed_at: datetime = datetime.now()

    def __contains__(self, obj: Any) -> bool:
        result = (
            obj in self._objects
            if isinstance(obj, EnvironmentVariable)
            else False
        )
        return result

    @property
    def keys(self) -> Optional[Sequence[Any]]:
        """Keys."""
        results = sorted(obj.reference for obj in self._objects)
        return results

    def add(self, obj: Any, /) -> None:
        """Add environment variable.

        Args:
            obj: Environment variable.

        Raises:
            TypeError: when argument is not type ``EnvironmentVariable``.

        """
        if not isinstance(obj, EnvironmentVariable):
            expected = "expected type 'EnvironmentVariable'"
            actual = f"got {type(obj)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if self.can_add(obj):
            self._objects.add(obj)

    def can_add(self, obj: Any) -> bool:
        """Check whether environment variable can be added.

        Args:
            obj: Environment variable.

        Raises:
            TypeError: when argument is not type ``EnvironmentVariable``.

        """
        errors.raise_for_instance(obj, EnvironmentVariable)
        result = obj not in self._objects
        return result

    def get(self, ref: str) -> Optional[EnvironmentVariable]:
        """Get environment variable.

        Args:
            ref: Reference for environment variable.

        Returns:
            Environment Variable.

        """
        try:
            result = next(
                obj
                for obj in self._objects
                if ref.upper() == obj.reference.upper()
            )
        except StopIteration:
            return None

        return result

    def list(self) -> List[EnvironmentVariable]:
        """List environment variables.

        Returns:
            Environment Variables.

        """
        key = operator.attrgetter("reference")
        results = sorted(self._objects, key=key)
        return results

    def remove(self, obj: Any, /) -> None:
        """Remove environment variable.

        Args:
            obj: Environment variable.

        Raises:
            TypeError: when argument is not type ``EnvironmentVariable``.

        """
        errors.raise_for_instance(obj, EnvironmentVariable)
        if obj in self._objects:
            var = self.get(getattr(obj, "reference"))
            setattr(var, "_removed_at", datetime.now())

    def commit(self) -> None:
        """Commit values in repository."""
        self._add_environment_variables()
        self._update_environment_variables()
        self._remove_environment_variables()
        self._committed_at = datetime.now()

    def _add_environment_variables(self) -> None:
        """Add variables to environment."""
        for obj in self._objects:
            if obj.created_at > self._committed_at:
                self._add_to_environment(obj)

    def _add_to_environment(self, obj: EnvironmentVariable) -> None:
        """Add variable to environment.

        Args:
            obj: Environment variable.

        """
        self._session[obj.reference] = str(obj.value)

    def _remove_environment_variables(self) -> None:
        """Remove variables to environment."""
        removed_variables = [obj for obj in self._objects if obj.is_removed]
        for obj in removed_variables:
            if obj.removed_at and obj.removed_at > self._committed_at:
                self._remove_from_environment(obj)

    def _remove_from_environment(self, obj: EnvironmentVariable) -> None:
        """Remove variable from environment.

        Args:
            obj: Environment variable.

        """

        del self._session[obj.reference]

    def _update_environment_variables(self) -> None:
        """Update variables to environment."""
        updated_variables = [obj for obj in self._objects if obj.is_updated]
        print(self._objects)
        print(updated_variables)
        for obj in updated_variables:
            if obj.updated_at and obj.updated_at > self._committed_at:
                self._update_in_environment(obj)

    def _update_in_environment(self, obj: EnvironmentVariable) -> None:
        """Update variable in environment.

        Args:
            obj: Environment variable.

        """
        self._session[obj.reference] = str(obj.value)

    def rollback(self) -> None:
        """Rollback values in repository."""
        self.load()

    def load(self) -> None:
        """Load environment variables."""
        self._objects = set(
            EnvironmentVariable(key, value)
            for key, value in self._session.items()
        )
