# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from pathlib import Path
from packaging.version import Version

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron import models


def test_setting_filepath_adds_version() -> None:
    filepath = Path("/test-0.0.1-any-none.whl")
    package = models.Package("test", filepath=filepath)
    result = package.version
    expected = Version("0.0.1")
    assert result == expected
