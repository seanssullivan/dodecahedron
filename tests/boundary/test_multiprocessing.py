# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
from multiprocessing.synchronize import Lock as LockCls
from multiprocessing import Lock
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Queue
from random import randint
import time
from typing import Any

# Third-Party Imports
import pytest


def put_func(q: "Queue[Any]") -> None:
    q.put([42, None, "hello"])


def print_func(name: str) -> None:
    print("hello", name)


def print_func_with_lock(l: LockCls, i: int):
    l.acquire()
    print(f"Running process {i}")
    try:
        time.sleep(randint(0, 10) / 100)
        print_func("Process " + str(i))
        time.sleep(randint(0, 10) / 100)
        print("hello world", i)
    finally:
        l.release()


def multiply_func(x: int) -> int:
    return x * x


def test_pool() -> None:
    with Pool(5) as p:
        print(p.map(multiply_func, [1, 2, 3]))

    assert False


def test_lock() -> None:
    lock = Lock()

    print(print_func_with_lock.__module__)
    print(print_func_with_lock.__name__)
    for num in range(10):
        p = Process(target=print_func_with_lock, args=(lock, num))
        print(f"Starting process {num}")
        p.start()

    time.sleep(2)
    assert False


def test_process() -> None:
    p = Process(target=print_func, args=("bob",))
    p.start()
    print(p.is_alive())
    p.join()

    print(p.is_alive())

    assert False


def test_pool_cannot_pickle_local_objects() -> None:
    def func(x: int) -> int:
        return x * x

    with pytest.raises(AttributeError), Pool(5) as p:
        p.map(func, [1, 2, 3])


def test_pool_cannot_pickle_lambda_functions() -> None:
    with pytest.raises(AttributeError), Pool(5) as p:
        p.map(lambda x: x * x, [1, 2, 3])


def test_queue() -> None:
    q: Queue[Any] = Queue()
    p = Process(target=put_func, args=(q,))
    p.start()
    p.join()
    print(q.get())  # prints "[42, None, 'hello']"
    assert False
