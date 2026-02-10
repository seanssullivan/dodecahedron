# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from argparse import ArgumentParser
from typing import Optional
from unittest.mock import Mock

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.cli import CommandLineInterface


def test_cli_calls_process_function() -> None:
    process = Mock()
    cli = CommandLineInterface(ArgumentParser(), {"run": process})
    cli.execute(["run"])

    process.assert_called_once()


def test_cli_passes_positional_arguments_to_process_function() -> None:
    result: Optional[str] = None

    def process(value: str, /) -> None:
        nonlocal result
        result = value

    cli = CommandLineInterface(ArgumentParser(), {"test": process})
    cli.parser.add_argument("value", type=str, choices=["failure", "success"])
    cli.execute(["test", "success"])

    assert result == "success"


def test_cli_passes_keyword_arguments_to_process_function() -> None:
    result: Optional[str] = None

    def process(*, value: str = "failure") -> None:
        nonlocal result
        result = value

    cli = CommandLineInterface(ArgumentParser(), {"test": process})
    cli.parser.add_argument("value", type=str, choices=["failure", "success"])
    cli.execute(["test", "success"])

    assert result == "success"
