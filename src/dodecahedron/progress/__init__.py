# -*- coding: utf-8 -*-

# Standard Library Imports
import importlib

# Local Imports
from .abstract_progress_bar import *

try:
    importlib.import_module("tqdm")
except (ImportError, ModuleNotFoundError):
    pass
else:
    from .tqdm_progress_bar import *
