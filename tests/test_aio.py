import asyncio
import pytest
from asyncio import Event
from contextvars import ContextVar
import aiocontextvars  # noqa: F401


v = ContextVar('v')


@pytest.mark.asyncio
async def parallel(x):
    v.set(x)
    await asyncio.sleep(0.1)
    assert v.get() == x


@pytest.mark.asyncio
async def test_parallel():
    await asyncio.gather(*map(parallel, range(16)))


# noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_parallel_with_inherit():
    await asyncio.gather(*map(parallel, range(16)))


# noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_inherit():
    v.set('initial')

    async def sub():
        assert v.get('default') == 'initial'
        v.set('sub')
    fut = asyncio.ensure_future(sub())
    v.set('update')
    await asyncio.sleep(0.1)
    await fut
    assert v.get('default') == 'update'


# noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_inherit_call_soon():
    v.set('initial')

    event = Event()

    def sub(arg1, arg2):
        try:
            assert v.get('default') == 'initial'
            assert arg1 == 'arg1'
            assert arg2 == 'arg2'
            v.set('sub')
        finally:
            event.set()

    loop = asyncio.get_event_loop()
    loop.call_soon(sub, 'arg1', 'arg2')
    v.set('update')

    await asyncio.sleep(0.1)
    await event.wait()
    assert v.get('default') == 'update'

# noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_inherit_call_later():
    v.set('initial')

    event = Event()

    def sub():
        try:
            assert v.get('default') == 'initial'
            v.set('sub')
        finally:
            event.set()

    loop = asyncio.get_event_loop()
    loop.call_later(0.5, sub)
    v.set('update')

    await event.wait()
    assert v.get('default') == 'update'


def test_set_event_loop_none():
    # Setting event loop to None should not raise an exception
    asyncio.set_event_loop(None)
