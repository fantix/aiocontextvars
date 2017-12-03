==============
aiocontextvars
==============

.. image:: https://img.shields.io/pypi/v/aiocontextvars.svg
        :target: https://pypi.python.org/pypi/aiocontextvars

.. image:: https://img.shields.io/travis/fantix/aiocontextvars.svg
        :target: https://travis-ci.org/fantix/aiocontextvars

This library offers the "thread local" for Python asyncio, also known as "task
local".

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

This is a partial PEP-550 polyfill.

PEP-550 proposed a consistent way across threads, generators and asyncio
``Task``s, to manage execution context, which is a kind of shared storage as
the context of such executions, with which one could share data within the same
execution without passing the data around as function parameters. A close
example of such context is ``threading.local``, which offers different data
space for different threads. It is obvious that ``threading.local`` cannot be
used for e.g. ``Task`` because usually all coroutines are scheduled within the
same thread, generators are similar. That's the main motivation of PEP-550.
However there's been so much discussion around this PEP about all kinds of
possibilities and cases, and it couldn't get accepted in a short while, thus we
decided to come up with this project, trying to solve a subset of all the
problems PEP-550 tried to solve, which is, as its name indicates, to implement
a contextual storage for asyncio ``Task``. We tried to build API that is
compatible with the latest discussion and most possible direction, so that the
cost to migrate code to future accepted PEP-550 may be minimized - just replace
the import with:

.. code-block:: python

   try:
       from contextvars import ContextVar
   except ImportError:
       from aiocontextvars import ContextVar, enable_inherit
       enable_inherit()


Inheritance
-----------

A key feature of ``ContextVar`` is the ability to inherit data across
``Task``s. When creating a new ``Task`` within another ``Task`` which had a
``ContextVar`` set, the new ``Task`` shall inherit the ``ContextVar`` values
from the parent ``Task``. However any changes to the context variables made in
the parent task after the child task was spawned are not visible to the child
task. The reason is explained in PEP-550_ - common usage intent and backwards
compatibility. Please follow the link and read more there. Here's a simple
example of inheritance:

.. code-block:: python

   import asyncio
   from aiocontextvars import ContextVar, enable_inherit

   var = ContextVar('my_variable')

   async def main():
       var.set('main')
       loop.create_task(sub())
       assert var.get() == 'main'
       var.set('main changed')
       await asyncio.sleep(2)
       assert var.get() == 'main changed'

   async def sub():
       assert var.get() == 'main'
       await asyncio.sleep(1)
       assert var.get() == 'main'
       var.set('sub')

   loop = asyncio.get_event_loop()
   enable_inherit(loop)
   loop.run_until_complete(main())

Please be noted that, the inheritance feature needs to be enabled explicitly
when using aiocontextvars, while it is a builtin feature for PEP-550. Because
aiocontextvars needs to hack the task factory of a given loop to achieve
inheritance, so if a custom task factory is needed, make sure it is installed
before enabling inheritance. It is also possible to disable inheritance and
remove the task factory hack by calling ``disable_inherit``. Meanwhile the
return value of ``enable_inherit`` is a PEP-343 context, you can do something
like this to minimize the impact:

.. code-block:: python

   from aiocontextvars import enable_inherit

   with enable_inherit():
       loop.create_task(main())

Or even ``aiocontextvars.create_task`` can be used as a short of this:

.. code-block:: python

   from aiocontextvars import create_task

   create_task(main(), loop=loop)

Sometimes it is useful to know whether current ``ContextVar`` is inheriting
from parent or not. This information is available through ``Context.inherited``:

.. code-block:: python

   from aiocontextvars import Context

   if Context.current().inherited:
       print('Inherited!')


Credits
-------

Fantix King is the author and maintainer of this library. ``var.py`` is
modified based on Guido's ``pep550/simpler.py``_. This library is open source
software under BSD license.

.. _PEP-550: https://www.python.org/dev/peps/pep-0550/#coroutines-and-asynchronous-tasks
.. _``pep550/simpler.py``: https://git.io/vbOeS
