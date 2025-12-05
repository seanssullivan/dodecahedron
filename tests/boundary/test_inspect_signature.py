# -*- coding: utf-8 -*-

# Standard Library Imports
import inspect


def test_selects_positional_only_arguments() -> None:
    def func(success: str, /) -> None: ...

    signature = inspect.signature(func)
    parameters = signature.parameters
    results = [
        name
        for name, param in parameters.items()
        if param.kind.name == "POSITIONAL_ONLY"
    ]
    assert results == ["success"]


def test_selects_positional_or_keyword_arguments() -> None:
    def func(success: str) -> None: ...

    signature = inspect.signature(func)
    parameters = signature.parameters
    results = [
        name
        for name, param in parameters.items()
        if param.kind.name == "POSITIONAL_OR_KEYWORD"
    ]
    assert results == ["success"]


def test_selects_keyword_only_arguments() -> None:
    def func(*, success: str) -> None: ...

    signature = inspect.signature(func)
    parameters = signature.parameters
    results = [
        name
        for name, param in parameters.items()
        if param.kind.name == "KEYWORD_ONLY"
    ]
    assert results == ["success"]
