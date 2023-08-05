Context Managers for Controlling Exception Chaining
===================================================

Provides a different way of controlling exception chaining
(the implicit ``__context__`` and explicit ``__cause__``)
beyond just ``raise ... from ...``.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install exceptioncontext


Usage
-----

Import as needed:

.. code:: python

    from exceptioncontext import cause, context, suppress_context

Explicitly chain exception (set ``__cause__``):

.. code:: python

    with cause(Exception("foo")):
        raise Exception("bar")

Override implicitly chained exception (set ``__context__``):

.. code:: python

    with context(Exception("foo")):
        raise Exception("bar")

Manually control context suppression (set ``__suppress_context__``):

.. code:: python

    with suppress_context(False):
        raise Exception("foo")

Reduce repetition in code like

.. code:: python

    if some_condition:
        raise SomeError("foo") from earlier_exception
    elif other_condition:
        raise OtherError("bar") from earlier_exception
    else:
        raise Exception("qux") from earlier_exception

by turning it into

.. code:: python

    with context(earlier_exception):
        if some_condition:
            raise SomeError("foo")
        elif other_condition:
            raise OtherError("bar")
        else:
            raise Exception("qux")

You now have more freedom in refactoring exception logic,
because chaining is fully independent of the ``raise``
statement, and freely composable with other code:

.. code:: python

    with cause(earlier_exception):
        helper_function()


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

(The oldest tested is 2.5, but it will likely work as far
back as 2.2 when paired with something like |with|_.)

.. |with| replace:: ``with-as-a-function``
.. _with: https://pypi.org/with-as-a-function

On implementations of Python where setting the exception chaining
attributes on an exception raises an ``AttributeError``,
``exceptioncontext`` gracefully degrades to doing nothing.
