import pytest
from aiocontextvars import enable_inherit


@pytest.fixture
def inherit(event_loop):
    with enable_inherit(event_loop):
        yield
