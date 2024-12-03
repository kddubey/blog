"""
Almost-working automation which overloads functions sharing a common signature. Not
useful b/c it doesn't work w/ @wraps, which is a dealbreaker to me.
"""

from functools import wraps
from typing import overload


def decorator(func):
    @overload
    def wrapper(x: str) -> int: ...

    @overload
    def wrapper(x: list[str]) -> list[int]: ...

    # Unfortunately, applying this decorator breaks the types :-(
    # Fixing it isn't enough. I want to simultaneously keep func.__annotations__ for
    # everything that's not x / I want it to work when there are other inputs which I
    # don't care about.
    # @wraps(
    #     func,
    #     assigned=(
    #         "__module__",
    #         "__name__",
    #         "__qualname__",
    #         "__doc__",
    #     ),
    # )
    def wrapper(x: str | list[str]) -> int | list[int]:
        return func(x)

    return wrapper


@decorator
def func(x: str | list[str]) -> int | list[int]:
    """
    _summary_

    Parameters
    ----------
    x : str | list[str]
        _description_

    Returns
    -------
    int | list[int]
        _description_
    """
    if isinstance(x, str):
        return 0
    return list(range(len(x)))


int_ = func("string")  # hovering over int_ should say it's int
list_int = func(["list"])  # hovering over list_int should say it's list[int]
