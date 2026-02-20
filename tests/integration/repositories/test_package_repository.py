# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.models import Package
from dodecahedron.repositories import PackageRepository


def test_adds_package_to_repository() -> None:
    repo = PackageRepository()
    pkg = Package("test")
    repo.add(pkg)
    assert pkg in repo


def test_gets_package_from_repository() -> None:
    repo = PackageRepository(packages=[Package("test")])
    result = repo.get("test")
    assert isinstance(result, Package)


def test_loads_packages_from_environment() -> None:
    repo = PackageRepository()
    repo.load()
    results = repo.list()
    assert len(results) != 0
