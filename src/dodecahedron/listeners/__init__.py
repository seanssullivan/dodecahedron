# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
from .abstract_listener import *

try:
    importlib.import_module("redis")
except (ImportError, ModuleNotFoundError):
    pass
else:
    from .redis_listener import *
