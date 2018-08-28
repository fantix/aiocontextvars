==============
aiocontextvars
==============

.. image:: https://img.shields.io/pypi/v/aiocontextvars.svg
        :target: https://pypi.python.org/pypi/aiocontextvars

.. image:: https://img.shields.io/travis/fantix/aiocontextvars.svg
        :target: https://travis-ci.org/fantix/aiocontextvars

**IMPORTANT:** This package will be deprecated after
`contextvars asyncio backport`_ is fixed.

This library is a compatibility wrapper of ``contextvars`` library introduced
in Python 3.7, or its backport for Python 3.5 and 3.6. It offers the "thread
local" for Python asyncio, also known as "task local".

Please read more in Python 3.7 [contextvars documentation](
https://docs.python.org/3/library/contextvars.html).

.. code-block:: python

   import asyncio
   from aiocontextvars import ContextVar

   var = ContextVar('my_variable')

   async def main():
       var.set('main')
       await sub()
       assert var.get() == 'sub'

   async def sub():
       assert var.get() == 'main'
       var.set('sub')
       assert var.get() == 'sub'

   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())

In above example, value ``main`` was stored in ``var``, and the following code
could then retrieve the value wherever ``var`` is available, without having to
pass this value around as parameter, e.g. in ``sub``. In the mean time, ``sub``
could also mutate the value, while being visible to its caller.

Different than a global variable and similar to thread local, a ``ContextVar``
keeps the different values set in different tasks, without messing up:

.. code-block:: python

   import asyncio
   from aiocontextvars import ContextVar

   var = ContextVar('my_variable')

   async def main(count):
       var.set(count)
       await asyncio.sleep(1)  # make sure all counts are set before assertion
       await sub(count)
       assert var.get() == count + 1

   async def sub(count):
       assert var.get() == count
       var.set(count + 1)
       assert var.get() == count + 1

   loop = asyncio.get_event_loop()

   tasks = []
   for i in range(8):
       tasks.append(loop.create_task(main(i)))

   loop.run_until_complete(asyncio.gather(*tasks))


With such, it is usually used to store non-global but shared states, e.g.
requests or database connections.


Compatibility
-------------

In Python 3.7 this package *is* 100% ``contextvars``.

In Python 3.5 and 3.6, this package added asyncio support to the PEP-567
backport package also named ``contextvars``, in a very different way than
Python 3.7 ``contextvars`` implementation:

1. ``call_soon()`` and family methods.

Python 3.7 added keyword argument ``context`` to ``call_soon()`` and its family
methods. By default those methods will copy (inherit) the current context and
run the given method in that context. But ``aiocontextvars`` won't touch the
loop, so in order to achieve the same effect, you'll need to::

    loop.call_soon(copy_context().run, my_meth)

2. Task local.

Python 3.7 used above keyword argument ``context`` in ``Task`` to make sure
that each step of a coroutine is ran in the same context inherited at the time
its driving task was created. Meanwhile, ``aiocontextvars`` uses
``Task.current_task()`` to achieve similar effect: it hacks asyncio and
attaches a copied context to the task on its creation, and replaces thread
local with current task instance to share the context. This behaves identically
to Python 3.7 in most times. What you need to do is to import
``aiocontextvars`` before creating loops.

3. Custom tasks and loops.

Because above hack is done by replacing ``asyncio.get_event_loop`` and
``loop.create_task``, therefore tasks and loops created by custom/private API
won't behave correctly as expected, e.g. ``uvloop.new_event_loop()`` or
``asyncio.Task()``. Also, event loops created before importing
``aiocontextvars`` are not patched either. So over all, you should import
``aiocontextvars`` at the beginning before creating event loops, and always use
``asyncio.*`` to operate loops/policies, and public asyncio API to create
tasks.


Credits
-------

Fantix King is the author and maintainer of this library. This library is open
source software under BSD license.

.. _contextvars asyncio backport: https://github.com/MagicStack/contextvars/issues/2
