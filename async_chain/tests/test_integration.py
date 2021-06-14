import pytest
import asyncio
import async_chain

pytestmark = pytest.mark.asyncio


class ExampleClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Example(value={self.value})"

    @async_chain.method
    async def plus(self, n):
        await asyncio.sleep(0)
        return self.__class__(self.value + n)

    @property
    @async_chain.method
    async def incremented(self):
        await asyncio.sleep(0)
        return self.__class__(self.value + 1)

    @async_chain.method
    async def triple_list(self):
        await asyncio.sleep(0)
        return [self.value, self.value + 1, self.value + 2]


async def test_class_creation():
    example = ExampleClass(0)
    assert example


@pytest.fixture()
def example():
    return ExampleClass(0)


async def test_method_existence(example):
    assert hasattr(example, "plus")
    assert hasattr(example, "incremented")
    assert hasattr(example, "triple_list")


async def test_chain_single_property(example):
    one = await example.incremented
    assert isinstance(one, ExampleClass)
    assert one.value == 1


async def test_chain_multiple_properties(example):
    three = await example.incremented.incremented.incremented
    assert isinstance(three, ExampleClass)
    assert three.value == 3


async def test_chain_single_method(example):
    one = await example.plus(1)
    assert isinstance(one, ExampleClass)
    assert one.value == 1


async def test_chain_multiple_methods(example):
    three = await example.plus(1).plus(1).plus(1)
    assert isinstance(three, ExampleClass)
    assert three.value == 3


async def test_chain_getitem(example):
    two = await example.triple_list()[2]
    assert isinstance(two, int)
    assert two == 2
