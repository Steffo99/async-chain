import inspect
import typing as t
import abc


class Chain(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    def __getattr__(self, item):
        return ChainGetAttr(previous=self, item=item)

    def __getitem__(self, item):
        return ChainGetItem(previous=self, item=item)

    def __call__(self, *args, **kwargs):
        return ChainCall(previous=self, args=args, kwargs=kwargs)

    def __await__(self):
        return self.__evaluate__().__await__()

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __display__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    async def __evaluate__(self):
        raise NotImplementedError()


class ChainStart(Chain):
    def __init__(self, start: t.Any):
        super().__init__()
        self.__start__: t.Any = start

    def __repr__(self):
        return f"<Chain {self.__display__()}>"

    def __display__(self):
        return f"{self.__start__!r}"

    async def __evaluate__(self):
        return self.__start__


class ChainNode(Chain, metaclass=abc.ABCMeta):
    def __init__(self, previous: Chain):
        super().__init__()
        self.__previous__: Chain = previous

    def __repr__(self):
        return f"<Chain {self.__display__()}>"


class ChainGetAttr(ChainNode):
    def __init__(self, previous: Chain, item: str):
        super().__init__(previous=previous)
        self._item: str = item

    def __display__(self):
        return f"{self.__previous__.__display__()}.{self._item!s}"

    async def __evaluate__(self):
        previous = await self.__previous__.__evaluate__()

        current = getattr(previous, self._item)

        if inspect.isawaitable(current):
            return await current
        else:
            return current


class ChainGetItem(ChainNode):
    def __init__(self, previous: Chain, item: t.Any):
        super().__init__(previous=previous)
        self._item: t.Any = item

    def __display__(self):
        return f"{self.__previous__.__display__()}[{self._item!r}]"

    async def __evaluate__(self):
        previous = await self.__previous__.__evaluate__()

        current = previous[self._item]

        if inspect.isawaitable(current):
            return await current
        else:
            return current


class ChainCall(ChainNode):
    def __init__(self, previous: Chain, args, kwargs):
        super().__init__(previous=previous)
        self._args = args
        self._kwargs = kwargs

    def __display__(self):
        args = map(lambda a: f"{a!r}", self._args)
        kwargs = map(lambda k, v: f"{k!s}={v!r}", self._kwargs)
        allargs = ", ".join([*args, *kwargs])
        return f"{self.__previous__.__display__()}({allargs})"

    async def __evaluate__(self):
        previous = await self.__previous__.__evaluate__()

        current = previous(*self._args, **self._kwargs)

        if inspect.isawaitable(current):
            return await current
        else:
            return current
