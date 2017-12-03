import asyncio

from .context import Context


class TaskFactory:
    __slots__ = ('_loop', '_orig_factory')

    def __init__(self, loop):
        self._loop = loop
        self._orig_factory = loop.get_task_factory()
        self._loop.set_task_factory(self)

    def uninstall(self):
        self._loop.set_task_factory(self._orig_factory)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.uninstall()

    def __call__(self, loop, coro):
        assert loop is self._loop
        loop.set_task_factory(self._orig_factory)
        try:
            task = loop.create_task(coro)

            if getattr(task, '_source_traceback', None):
                del getattr(task, '_source_traceback')[-2:]

            task.ctx = Context(Context.current())

            return task
        finally:
            loop.set_task_factory(self)


def enable_inherit(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    return TaskFactory(loop)


def disable_inherit(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    getattr(loop.get_task_factory(), 'uninstall', lambda: None)()


def create_task(coro, *, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    with enable_inherit(loop):
        return loop.create_task(coro)
