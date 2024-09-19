# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.mappers import ClassMapper


class ExampleClass:
    """An example implementation of a model class.

    Args:
        value: Value.

    Raises:
        ValueError: when argument is ``None``.

    """

    def __init__(self, value: typing.Any = None) -> None:
        if value is None:
            raise ValueError("argument cannot be 'None'")

        self._value = value

    @property
    def value(self) -> typing.Any:
        """Value"""
        return self._value


def test_instantiates_class_from_dictionary() -> None:
    mapper = ClassMapper(ExampleClass, {}, {"_value": "value"})
    result = mapper.from_dict({"value": "success"})
    assert isinstance(result, ExampleClass)
    assert result.value == "success"


def test_instantiates_class_from_list() -> None:
    mapper = ClassMapper(ExampleClass, {}, {"_value": 0})
    result = mapper.from_dict(["success"])
    assert isinstance(result, ExampleClass)
    assert result.value == "success"
