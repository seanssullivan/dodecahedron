# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib  # pragma: no cover

# Local Imports
from .abstract_dispatcher import *

try:  # pragma: no cover
    importlib.import_module("tqdm")
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .progressive_dispatcher import *
