# -*- coding: utf-8 -*-

# Local Imports
from .singleton import SingletonMeta
from .tracker import TrackerMeta

__all__ = ["RepositoryMeta"]


class RepositoryMeta(SingletonMeta, TrackerMeta):
    """Implements a repository metaclass.

    Combines the singleton and tracker metaclasses into a single metaclass
    for use by repositories.

    """
