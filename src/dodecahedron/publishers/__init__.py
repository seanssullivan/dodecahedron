# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
from .abstract_publisher import *

try:
    importlib.import_module("redis")  # pragma: no cover
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .redis_publisher import *
