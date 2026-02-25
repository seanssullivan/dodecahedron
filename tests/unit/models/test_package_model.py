# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from pathlib import Path
from packaging.version import Version
from typing import Generator

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron import models


@pytest.fixture
def version(request: pytest.FixtureRequest) -> Generator[Version, None, None]:
    result = Version(request.param)
    yield result


def test_setting_filepath_adds_version() -> None:
    filepath = Path("/test-0.0.1-any-none.whl")
    package = models.Package("test", filepath=filepath)
    result = package.version
    expected = Version("0.0.1")
    assert result == expected


@pytest.mark.parametrize("version", ["0.0.1.dev1"], indirect=True)
def test_returns_true_when_dev_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_dev_release is True


@pytest.mark.parametrize("version", ["0.0.1b1", "0.0.1"], indirect=True)
def test_returns_false_when_not_dev_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_dev_release is False


@pytest.mark.parametrize("version", ["0.0.1"], indirect=True)
def test_returns_true_when_final_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_final_release is True


@pytest.mark.parametrize("version", ["0.0.1.dev1", "0.0.1b1"], indirect=True)
def test_returns_false_when_not_final_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_final_release is False


@pytest.mark.parametrize("version", ["0.0.1a1", "0.0.1b2"], indirect=True)
def test_returns_true_when_pre_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_pre_release is True


@pytest.mark.parametrize("version", ["0.0.1.dev1", "0.0.1"], indirect=True)
def test_returns_false_when_not_pre_release(version: Version) -> None:
    package = models.Package("test", version=version)
    assert package.is_pre_release is False
