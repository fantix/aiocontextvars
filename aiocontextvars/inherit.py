import asyncio

from .context import Context

_original_task_factories = {}


def _task_factory(loop, coro):
    loop.set_task_factory(_original_task_factories.get(loop))
    try:
        task = loop.create_task(coro)

        if getattr(task, '_source_traceback', None):
            del getattr(task, '_source_traceback')[-2:]

        task.ctx = Context.current().copy()

        return task
    finally:
        loop.set_task_factory(_task_factory)


class InheritContext:

    __slots__ = ('_loop',)

    def __init__(self, loop):
        self._loop = loop

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        disable_inherit(self._loop)


def enable_inherit(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    if loop in _original_task_factories:
        return
    _original_task_factories[loop] = loop.get_task_factory()
    loop.set_task_factory(_task_factory)
    return InheritContext(loop)


def disable_inherit(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    if loop in _original_task_factories:
        loop.set_task_factory(_original_task_factories.pop(loop))
