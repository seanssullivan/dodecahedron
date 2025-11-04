# -*- coding: utf-8 -*-
"""Repositories.

Todo:
    * Add 'sqlite3' repository.

"""

# Standard Library Imports
import importlib

# Local Imports
from .abstract_repository import *
from .csv_repository import *
from .eventful_repository import *
from .txt_repository import *

try:
    importlib.import_module("sqlalchemy")
except (ImportError, ModuleNotFoundError):
    pass
else:
    from .sqlalchemy_repository import *

try:
    importlib.import_module("openpyxl")
except (ImportError, ModuleNotFoundError):
    pass
else:
    from .xlsx_repository import *
