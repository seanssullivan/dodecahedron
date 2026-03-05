# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any
from typing import List
from typing import Optional

# Local Imports
from .abstract_repository import AbstractRepository

__all__ = ["EnvironmentRepository"]


class EnvironmentRepository(AbstractRepository):
    """Class implements an environment repository."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __contains__(self, obj: Any) -> bool:
        raise NotImplementedError

    def add(self, obj: Any, /) -> None:
        """Add variable.

        Args:
            obj: Variable.

        Raises:
            TypeError: when argument is not type ``str`` or ``tuple``.

        """
        raise NotImplementedError

    def can_add(self, obj: Any) -> bool:
        """Check whether variable can be added.

        Args:
            obj: Variable.

        Raises:
            TypeError: when argument is not type ``str``.

        """
        if not isinstance(obj, str):
            message = f"expected type 'Package', got {type(obj)} instead"
            raise TypeError(message)

        raise NotImplementedError

    def get(self, ref: str, /) -> Optional[str]:
        """Get variable.

        Args:
            ref: Reference for variable.

        Returns:
            Variable.

        """
        raise NotImplementedError

    def list(self) -> List[str]:
        """List variables.

        Returns:
            Variables.

        """
        raise NotImplementedError

    def load(self) -> None:
        """Load variables from environment."""
        raise NotImplementedError

    def remove(self, obj: Any, /) -> None:
        """Remove variable.

        Args:
            obj: Variable.

        Raises:
            TypeError: when argument is not type ``str``.

        """
        if not isinstance(obj, str):
            message = f"expected type 'str', got {type(obj)} instead"
            raise TypeError(message)

        raise NotImplementedError

    def commit(self) -> None:
        """Commit values in repository."""

    def rollback(self) -> None:
        """Rollback values in repository."""


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_variable_in_environment(__name: str, /) -> Optional[str]:
    """Get variable in environment.

    Args:
        __name: Name of variable.

    Returns:
        Variable.

    """
    raise NotImplementedError


def list_variables_in_environment() -> List[str]:
    """List variables in environment.

    Returns:
        Variables.

    """
    results: List[str] = []
    return results
