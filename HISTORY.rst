=======
History
=======

0.2.1 (2018-10-24)
------------------

* Changed to single module layout.
* Updated README.

0.2.0 (2018-09-09)
------------------

**This is a breaking change.** Most implementation is replaced with
``contextvars``. In Python 3.5 and 3.6, ``aiocontextvars`` depends on
``contextvars`` the PEP-567 backport in PyPI, and patches it to partially
support asyncio; in Python 3.7 ``aiocontextvars`` is only a delegate to the
built-in ``contextvars`` library.

* Modified ``ContextVar.set()`` to return a token.
* Added ``ContextVar.reset(token)``.
* Removed ``ContextVar.delete()``.
* Removed ``enable_inherit()`` and ``disable_inherit()``, inherit is always enabled.
* Added ``copy_context()`` and ``Context.run()``.
* Removed ``Context.current()`` and ``Context.inherited``.
* Fixed issue that ``set_event_loop(None)`` fails (contributed by J.J. Jackson in #10 #11)

0.1.2 (2018-04-04)
------------------

* Supported Python 3.5.

0.1.1 (2017-12-03)
------------------

* Fixed setup.py

0.1.0 (2017-12-03)
------------------

* First release on PyPI.
