import asyncio
import pytest
from aiocontextvars import ContextVar

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


def test_set_event_loop_none():
    # Setting event loop to None should not raise an exception
    asyncio.set_event_loop(None)
