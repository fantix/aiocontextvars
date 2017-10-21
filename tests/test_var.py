import pytest
from aiocontextvars import ContextVar


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
    v.set(123)
    assert v.get() == 123
    assert v.get(789) == 123
    return v


def test_set_with_default():
    v = test_get_with_default()
    v.set(789)
    assert v.get() == 789
    assert v.get(0) == 789
    return v


def test_same_name():
    v1 = ContextVar('v')
    v2 = ContextVar('v')
    v1.set(1)
    v2.set(2)
    assert v1.get() == 1
    assert v2.get() == 2


def test_delete():
    v = test_set()
    v.delete()
    with pytest.raises(LookupError):
        v.get()
    assert v.get(456) == 456
    with pytest.raises(LookupError):
        v.delete()


def test_delete_with_default():
    v = test_set_with_default()
    for _ in range(3):
        v.delete()
        assert v.get() == 123
        assert v.get(0) == 0
