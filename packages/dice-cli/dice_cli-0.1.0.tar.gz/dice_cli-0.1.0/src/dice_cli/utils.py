from itertools import count
from typing import Iterable, Iterator


def current_linux_user() -> str:
    """Returns current user name"""
    import os

    return os.getlogin()


def current_date() -> str:
    """Returns big-endian string of the current date"""
    import datetime

    return datetime.datetime.now().strftime("%Y-%m-%d")


def current_fqdn() -> str:
    """Returns fully-qualified domain main (FQDN) of current machine"""
    import socket

    return socket.getfqdn()


def as_range(iterable: Iterable[int]) -> str:
    """From https://codereview.stackexchange.com/q/5196
    If {iterable} has at least two elements, return '{first}-{last}', otherwise '{first}'.
    """
    items = list(iterable)
    if len(items) > 1:
        return f"{items[0]}-{items[-1]}"
    else:
        return f"{items[0]}"


def groupby_range(x: int, c: Iterator[int] = count()) -> int:
    return next(c) - x


def groupby_inverse_range(x: int, c: Iterator[int] = count()) -> int:
    return x - next(c)
