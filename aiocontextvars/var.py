from typing import *

from .context import Context

T = TypeVar('T')
_no_default: Any = object()


class ContextVar(Generic[T]):
    """Context variable.

    Based on: https://git.io/vbOeS
    """

    __slots__ = ('_name', '_default', '__weakref__')

    def __init__(self, name: str, *, default: T = _no_default) -> None:
        self._name = name
        self._default = default

    @property
    def name(self) -> str:
        return self._name

    @property
    def default(self) -> T:
        return self._default

    # Methods that take the current context into account.

    def get(self, default: T = _no_default) -> T:
        """Return current value."""
        ctx: Context = Context.current()
        if self in ctx:
            return ctx[self]
        if default is not _no_default:
            return default
        if self._default is not _no_default:
            return self._default
        raise LookupError

    def set(self, value: T) -> None:
        """Overwrite current value."""
        ctx: Context = Context.current()
        ctx[self] = value

    def delete(self) -> None:
        """Delete current value."""
        ctx: Context = Context.current()
        if self in ctx:
            del ctx[self]
        elif self._default is not _no_default:
            pass
        else:
            raise LookupError
