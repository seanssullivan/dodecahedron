# -*- coding: utf-8 -*-

# Standard Library Imports
import os
from typing import Optional

__all__ = [
    "is_development_environment",
    "is_production_environment",
    "is_staging_environment",
    "is_test_environment",
    "get_environment",
]


def is_development_environment() -> bool:
    """Check whether running in development environment.

    Returns:
        Whether running in development environment.

    """
    environment = get_environment()
    result = environment in ("dev", "development")
    return result


def is_production_environment() -> bool:
    """Check whether running in production environment.

    Returns:
        Whether running in production environment.

    """
    environment = get_environment()
    result = environment in ("prod", "production")
    return result


def is_staging_environment() -> bool:
    """Check whether running in staging environment.

    Returns:
        Whether running in staging environment.

    """
    environment = get_environment()
    result = environment == "staging"
    return result


def is_test_environment() -> bool:
    """Check whether running in test environment.

    Returns:
        Whether running in test environment.

    """
    environment = get_environment()
    result = environment == "test"
    return result


def get_environment() -> Optional[str]:
    """Get name of environment.

    Returns:
        Name of environment

    """
    value = os.environ.get("ENV")
    result = value.lower() if isinstance(value, str) else None
    return result
