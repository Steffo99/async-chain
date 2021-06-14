import functools
import typing as t
from .chain import ChainStart


class FunctionWrapper:
    def __init__(self, func):
        self._func = func

    def __repr__(self) -> str:
        return self._func.__name__

    def __call__(self, *args, **kwargs) -> t.Any:
        return self._func(*args, **kwargs)


def method_deco(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        return ChainStart(start=FunctionWrapper(func))(*args, **kwargs)
    return decorated
