# -*- coding: utf-8 -*-

# Standard Library Imports
import datetime
import decimal
import json
import pathlib
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Optional

# Local Imports
from .packages import import_module

# Optional Third-Party Imports
np = import_module("numpy", required=False)
pd = import_module("pandas", required=False)

__all__ = ["JSONEncoder"]


class JSONEncoder(json.JSONEncoder):
    """Class implements a custom JSON encoder."""

    def encode(self, o: Any, *args: Any, **kwargs: Any) -> str:
        """Return a JSON string representation of a Python data structure."""
        result = super().encode(replace_nan(o), *args, **kwargs)
        return result

    def default(self, o: object) -> Any:
        if isinstance(o, datetime.datetime):
            return str(o)

        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, pathlib.Path):
            return str(o.resolve())

        # Only check when numpy is installed.
        if np is not None and isinstance(o, getattr(np, "bool_")):
            return bool(o)

        # Only check when pandas is installed.
        if pd is not None and getattr(pd, "isnull")(o):
            return None

        return super().default(o)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def replace_nan(__value: Any, repl: Optional[str] = None) -> Any:
    """Replace 'np.nan'.

    Args:
        __value: Value in which to replace 'np.nan'.
        repl: Value with which to replace 'np.nan'.

    Returns:
        Value.

    """
    if isinstance(__value, dict):
        result: Dict[Hashable, Any] = {
            k: replace_nan(v) for k, v in __value.items()  # type: ignore
        }
        return result

    if isinstance(__value, list):
        result = [replace_nan(i) for i in __value]  # type: ignore
        return result

    if pd and getattr(pd, "isnull")(__value):
        return repl

    return __value
