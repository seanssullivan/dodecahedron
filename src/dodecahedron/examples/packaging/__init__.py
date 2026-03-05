# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
try:
    importlib.import_module("packaging")  # pragma: no cover
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .package_model import *
    from .package_repository import *
