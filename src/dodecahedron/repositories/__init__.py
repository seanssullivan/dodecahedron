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
from .package_repository import *
from .txt_repository import *

try:
    importlib.import_module("sqlalchemy")  # pragma: no cover
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .sqlalchemy_repository import *

try:
    importlib.import_module("openpyxl")  # pragma: no cover
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
else:  # pragma: no cover
    from .xlsx_repository import *
