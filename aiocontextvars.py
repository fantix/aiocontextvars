"""Top-level package for aiocontextvars."""

__author__ = """Fantix King"""
__email__ = 'fantix.king@gmail.com'
__version__ = '0.2.1'

import sys

from contextvars import Context, ContextVar, Token, copy_context


if sys.version_info < (3, 7):
    import asyncio
    import contextvars
    import types
    from contextvars import _state

    def _get_context():
        state = _get_state()
        ctx = getattr(state, 'context', None)
        if ctx is None:
            ctx = Context()
            state.context = ctx
        return ctx

    def _set_context(ctx):
        state = _get_state()
        state.context = ctx

    def _get_state():
        loop = asyncio._get_running_loop()
        if loop is None:
            return _state
        task = asyncio.Task.current_task(loop=loop)
        return _state if task is None else task

    contextvars._get_context = _get_context
    contextvars._set_context = _set_context

    def create_task(loop, coro):
        task = loop._orig_create_task(coro)
        if task._source_traceback:
            del task._source_traceback[-1]
        task.context = copy_context()
        return task

    def call_soon(loop, callback, *args):
        if callback == Context.run:
            return loop._orig_call_soon(callback, *args)
        else:
            context = copy_context()
            return loop._orig_call_soon(context.run, lambda: callback(*args))

    def call_later(loop, delay, callback, *args):
        if callback == Context.run:
            return loop._orig_call_later(delay, callback, *args)
        else:
            context = copy_context()
            return loop._orig_call_later(
                delay, context.run, lambda: callback(*args))

    def call_at(loop, when, callback, *args):
        if callback == Context.run:
            return loop._orig_call_at(when, callback, *args)
        else:
            context = copy_context()
            return loop._orig_call_at(
                when, context.run, lambda: callback(*args))

    def _patch_loop(loop):
        if loop and not hasattr(loop, '_orig_create_task'):
            loop._orig_create_task = loop.create_task
            loop.create_task = types.MethodType(create_task, loop)
            loop._orig_call_soon = loop.call_soon
            loop.call_soon = types.MethodType(call_soon, loop)
            loop._orig_call_later = loop.call_later
            loop.call_later = types.MethodType(call_later, loop)
            loop._orig_call_at = loop.call_at
            loop.call_at = types.MethodType(call_at, loop)
        return loop

    def get_event_loop():
        return _patch_loop(_get_event_loop())

    def set_event_loop(loop):
        return _set_event_loop(_patch_loop(loop))

    def new_event_loop():
        return _patch_loop(_new_event_loop())

    _get_event_loop = asyncio.get_event_loop
    _set_event_loop = asyncio.set_event_loop
    _new_event_loop = asyncio.new_event_loop

    asyncio.get_event_loop = asyncio.events.get_event_loop = get_event_loop
    asyncio.set_event_loop = asyncio.events.set_event_loop = set_event_loop
    asyncio.new_event_loop = asyncio.events.new_event_loop = new_event_loop


__all__ = ('ContextVar', 'Context', 'Token', 'copy_context')
