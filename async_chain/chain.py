from __future__ import annotations
import inspect
import typing as t
import abc


class Chain(metaclass=abc.ABCMeta):
    __slots__ = []

    def __getattr__(self, item) -> ChainGetAttr:
        return ChainGetAttr(previous=self, item=item)

    def __getitem__(self, item) -> ChainGetItem:
        return ChainGetItem(previous=self, item=item)

    def __call__(self, *args, **kwargs) -> ChainCall:
        return ChainCall(previous=self, args=args, kwargs=kwargs)

    def __await__(self):
        return self.__evaluate__().__await__()

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def __display__(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    async def __evaluate__(self) -> t.Any:
        raise NotImplementedError()


StartingType = t.TypeVar("StartingType")


class ChainStart(Chain):
    __slots__ = ("__start__",)

    def __init__(self, start: StartingType):
        super().__init__()
        self.__start__: StartingType = start

    def __repr__(self) -> str:
        return f"<Chain {self.__display__()}>"

    def __display__(self) -> str:
        return f"{self.__start__!r}"

    async def __evaluate__(self) -> StartingType:
        return self.__start__


class ChainNode(Chain, metaclass=abc.ABCMeta):
    __slots__ = ("__previous__",)

    def __init__(self, previous: Chain):
        super().__init__()
        self.__previous__: Chain = previous

    def __repr__(self) -> str:
        return f"<Chain {self.__display__()}>"


class ChainGetAttr(ChainNode):
    __slots__ = ("__item__",)

    def __init__(self, previous: Chain, item: str):
        super().__init__(previous=previous)
        self.__item__: str = item

    def __display__(self) -> str:
        return f"{self.__previous__.__display__()}.{self.__item__!s}"

    async def __evaluate__(self) -> t.Any:
        previous = await self.__previous__.__evaluate__()

        current = getattr(previous, self.__item__)

        if inspect.isawaitable(current):
            return await current
        else:
            return current


class ChainGetItem(ChainNode):
    __slots__ = ("__item__",)

    def __init__(self, previous: Chain, item: t.Any):
        super().__init__(previous=previous)
        self.__item__: t.Any = item

    def __display__(self) -> str:
        return f"{self.__previous__.__display__()}[{self.__item__!r}]"

    async def __evaluate__(self) -> t.Any:
        previous = await self.__previous__.__evaluate__()

        current = previous[self.__item__]

        if inspect.isawaitable(current):
            return await current
        else:
            return current


class ChainCall(ChainNode):
    __slots__ = ("__args__", "__kwargs__",)

    def __init__(self, previous: Chain, args: t.Collection[t.Any], kwargs: t.Mapping[str, t.Any]):
        super().__init__(previous=previous)
        self.__args__: t.Collection[t.Any] = args
        self.__kwargs__: t.Mapping[str, t.Any] = kwargs

    def __display__(self) -> str:
        args = map(lambda a: f"{a!r}", self.__args__)
        kwargs = map(lambda k, v: f"{k!s}={v!r}", self.__kwargs__)
        allargs: str = ", ".join([*args, *kwargs])
        return f"{self.__previous__.__display__()}({allargs})"

    async def __evaluate__(self) -> t.Any:
        previous = await self.__previous__.__evaluate__()

        current = previous(*self.__args__, **self.__kwargs__)

        if inspect.isawaitable(current):
            return await current
        else:
            return current
