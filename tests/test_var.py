import pytest
from contextvars import ContextVar
import aiocontextvars  # noqa: F401


def test_get():
    v = ContextVar('v')
    with pytest.raises(LookupError):
        v.get()
    assert v.get(456) == 456
    return v


def test_get_with_default():
    v = ContextVar('v', default=123)
    assert v.get() == 123
    assert v.get(456) == 456
    return v


def test_set():
    v = test_get()
    token = v.set(123)
    assert v.get() == 123
    assert v.get(789) == 123
    return v, token


def test_set_with_default():
    v = test_get_with_default()
    token = v.set(789)
    assert v.get() == 789
    assert v.get(0) == 789
    return v, token


def test_same_name():
    v1 = ContextVar('v')
    v2 = ContextVar('v')
    v1.set(1)
    v2.set(2)
    assert v1.get() == 1
    assert v2.get() == 2


def test_reset():
    v, token = test_set()
    v.reset(token)
    with pytest.raises(LookupError):
        v.get()
    assert v.get(456) == 456
    with pytest.raises(RuntimeError):
        v.reset(token)


def test_delete_with_default():
    v, token = test_set_with_default()
    v.reset(token)
    assert v.get() == 123
    assert v.get(0) == 0
