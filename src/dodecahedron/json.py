# -*- coding: utf-8 -*-

# Standard Library Imports
import datetime
import json
import logging
import pathlib
from typing import Any

# Third-Party Imports
# TODO: Make numpy and pandas optional.
import numpy as np
import pandas as pd

__all__ = ["JSONEncoder"]


# Initiate logger.
log = logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    """Class implements a custom JSON encoder."""

    def encode(self, o: Any, *args: Any, **kwargs: Any) -> str:
        """Return a JSON string representation of a Python data structure."""
        return super().encode(remove_nan(o), *args, **kwargs)

    def default(self, o: object) -> Any:
        # TODO: Only check if pandas is installed.
        if pd.isnull(o):
            return None

        # TODO: Only check if numpy is installed.
        if isinstance(o, np.bool_):
            return bool(o)

        if isinstance(o, datetime.datetime):
            return str(o)

        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, pathlib.Path):
            return str(o.resolve())

        return super().default(o)


def remove_nan(obj: Any) -> Any:
    """Remove NaN."""
    if isinstance(obj, dict):
        return {key: remove_nan(value) for key, value in obj.items()}

    if isinstance(obj, list):
        return [remove_nan(item) for item in obj]

    if pd.isnull(obj):
        return None

    return obj
