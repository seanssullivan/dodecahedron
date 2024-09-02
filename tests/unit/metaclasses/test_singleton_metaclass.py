# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.metaclasses import SingletonMeta


def test_subclass_is_singleton() -> None:
    class Singleton(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Singleton()
    instance2 = Singleton()
    assert instance1 is instance2


def test_clears_subclasses() -> None:
    class Singleton(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Singleton()
    SingletonMeta.clear()

    instance2 = Singleton()
    assert instance1 is not instance2


def test_discards_subclasses() -> None:
    class Singleton(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Singleton()
    SingletonMeta.discard(Singleton)

    instance2 = Singleton()
    assert instance1 is not instance2


def test_separate_subclasses_are_different() -> None:
    class Singleton1(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    class Singleton2(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Singleton1()
    instance2 = Singleton2()
    assert instance1 is not instance2
