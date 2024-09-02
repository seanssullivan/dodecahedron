# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
from .abstract_dispatcher import *
from .base_dispatcher import *

try:
    importlib.import_module("tqdm")
except (ImportError, ModuleNotFoundError):
    pass
else:
    from .progressive_dispatcher import *
