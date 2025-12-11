# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
from .abstract_progress_bar import *

try:
    importlib.import_module("tqdm")  # pragma: no cover
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .tqdm_progress_bar import *
