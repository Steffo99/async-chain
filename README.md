<div align="center">

![](.media/icon-128x128_round.png)

# `async-chain`

A coroutine builder

</div>

## Links

[![PyPI](https://img.shields.io/pypi/v/async-chain)](https://pypi.org/project/async-chain)

## About

### The problem

Have you ever felt that the `await` syntax in Python was a bit clunky when chaining multiple methods together?

```python
async def on_message(event):
    message = await event.get_message()
    author = await message.get_author()
    await author.send_message("Hello world!")
```

Or even worse:

```python
async def on_message(event):
    (await (await (await event.get_message()).get_author()).send_message("Hello world!"))
```

`async-chain` is here to solve your problem!

```python
async def on_message(event):
    await event.get_message().get_author().send_message("Hello world!")
```

### The solution

First, install `async_chain` with your favorite package manager:

```console
$ pip install async_chain
```
```console
$ pipenv install async_chain
```
```console
$ poetry add async_chain
```

Then, add the `@async_chain.method` decorator to any async method you wish to make chainable, and the problem will be 
magically solved!

```python
import async_chain

class MyEvent:
    @async_chain.method
    async def get_message(self):
        ...
```
