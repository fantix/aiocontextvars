import threading
from asyncio import Task
from typing import *
from weakref import WeakKeyDictionary

_thread_local = threading.local()
T = TypeVar('T', bound='Context')


# noinspection PyAbstractClass
class Context(WeakKeyDictionary):

    __slots__ = ('_inherited',)

    def __init__(self, d=None) -> None:
        super().__init__(d)
        self._inherited = d is not None

    @property
    def inherited(self) -> bool:
        return self._inherited

    @classmethod
    def current(cls: Type[T]) -> T:
        """Return current context (creating it if necessary)."""
        local = Task.current_task() or _thread_local
        rv = getattr(local, 'ctx', None)
        if rv is None:
            # noinspection PyCallingNonCallable
            rv = local.ctx = cls()
        return rv
