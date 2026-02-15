# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import os

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron import environment


@pytest.mark.parametrize("env", ["dev", "development"])
def test_returns_true_when_development_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_development_environment()
    assert result is True


@pytest.mark.parametrize("env", ["production", "staging", "test"])
def test_returns_false_when_not_development_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_development_environment()
    assert result is False


@pytest.mark.parametrize("env", ["prod", "production"])
def test_returns_true_when_production_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_production_environment()
    assert result is True


@pytest.mark.parametrize("env", ["development", "staging", "test"])
def test_returns_false_when_not_production_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_production_environment()
    assert result is False


@pytest.mark.parametrize("env", ["staging"])
def test_returns_true_when_staging_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_staging_environment()
    assert result is True


@pytest.mark.parametrize("env", ["development", "production", "test"])
def test_returns_false_when_not_staging_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_staging_environment()
    assert result is False


@pytest.mark.parametrize("env", ["test"])
def test_returns_true_when_test_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_test_environment()
    assert result is True


@pytest.mark.parametrize("env", ["development", "production", "staging"])
def test_returns_false_when_not_test_environment(env: str) -> None:
    os.environ["ENV"] = env
    result = environment.is_test_environment()
    assert result is False
