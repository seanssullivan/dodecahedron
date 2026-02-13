# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import datetime
import json
import pathlib
from typing import Any

# Third-Party Imports
import numpy as np
import pandas as pd
import pytest

# Local Imports
from dodecahedron.json import JSONEncoder


def test_json_encoder_dumps_date() -> None:
    result = json.dumps({"value": datetime.date.today()}, cls=JSONEncoder)
    assert result is not None


def test_json_encoder_dumps_datetime() -> None:
    result = json.dumps({"value": datetime.datetime.now()}, cls=JSONEncoder)
    assert result is not None


def test_json_encoder_dumps_path() -> None:
    result = json.dumps({"value": pathlib.Path(".")}, cls=JSONEncoder)
    assert result is not None


@pytest.mark.parametrize("value", [np.bool_(True), np.bool_(False)])
def test_json_encoder_dumps_bool(value: Any) -> None:
    result = json.dumps({"value": value}, cls=JSONEncoder)
    assert result is not None


@pytest.mark.parametrize("value", [pd.NA, np.nan])
def test_json_encoder_dumps_na(value: Any) -> None:
    result = json.dumps({"value": value}, cls=JSONEncoder)
    assert result is not None


@pytest.mark.parametrize("value", [pd.NA, np.nan])
def test_json_encoder_converts_na_to_none(value: Any) -> None:
    data = json.dumps({"value": value}, cls=JSONEncoder)
    result = json.loads(data)
    assert result["value"] is None


@pytest.mark.parametrize("value", [pd.NaT, np.datetime64("NaT")])
def test_json_encoder_dumps_nat(value: Any) -> None:
    result = json.dumps({"value": value}, cls=JSONEncoder)
    assert result is not None


@pytest.mark.parametrize("value", [pd.NaT, np.datetime64("NaT")])
def test_json_encoder_converts_nat_to_none(value: Any) -> None:
    data = json.dumps({"value": value}, cls=JSONEncoder)
    result = json.loads(data)
    assert result["value"] is None
