# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import os
from typing import Generator

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.examples.environment import EnvironmentRepository
from dodecahedron.examples.environment import EnvironmentVariable


@pytest.fixture
def test_variable() -> None:
    """Fixture to set an environment variable."""
    os.environ["TEST"] = "success"


@pytest.fixture
def variable(
    request: pytest.FixtureRequest,
) -> Generator[EnvironmentVariable, None, None]:
    """Fixture to set an environment variable."""
    key, value = [*request.param]
    os.environ[key] = value
    yield EnvironmentVariable(key, value)


def test_adds_variable_to_repository() -> None:
    repo = EnvironmentRepository()
    var = EnvironmentVariable("test")
    repo.add(var)
    assert var in repo


@pytest.mark.usefixtures("test_variable")
def test_loads_variables_from_environment() -> None:
    repo = EnvironmentRepository()
    repo.load()
    results = repo.list()
    assert len(results) != 0


@pytest.mark.usefixtures("test_variable")
def test_gets_variable_from_repository() -> None:
    repo = EnvironmentRepository()
    result = repo.get("test")
    assert isinstance(result, EnvironmentVariable)


@pytest.mark.usefixtures("test_variable")
def test_removes_variable_from_repository() -> None:
    repo = EnvironmentRepository()
    var: EnvironmentVariable = repo.get("test")  # type: ignore
    repo.remove(var)
    assert var.is_removed


def test_adds_variable_to_environment() -> None:
    repo = EnvironmentRepository()
    var = EnvironmentVariable("result", "success")
    repo.add(var)
    repo.commit()
    assert os.environ["RESULT"] == "success"

    # Cleanup
    del os.environ["RESULT"]


def test_removes_variable_from_environment() -> None:
    repo = EnvironmentRepository()
    var = EnvironmentVariable("result", "success")
    repo.add(var)
    repo.commit()
    assert "RESULT" in os.environ

    repo.remove(var)
    repo.commit()
    assert "RESULT" not in os.environ


def test_updated_variable_in_environment() -> None:
    repo = EnvironmentRepository()
    var = EnvironmentVariable("result", "failure")
    repo.add(var)
    repo.commit()
    assert os.environ["RESULT"] == "failure"

    var.update("success")
    repo.commit()
    assert os.environ["RESULT"] == "success"

    # Cleanup
    del os.environ["RESULT"]
