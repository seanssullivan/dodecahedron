# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib  # pragma: no cover

# Local Imports
from .abstract_publisher import *

try:  # pragma: no cover
    importlib.import_module("redis")
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .redis_publisher import *
