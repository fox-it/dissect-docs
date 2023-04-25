dissect.target
==============

.. button-link:: https://github.com/fox-it/dissect.target
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

The Dissect module tying all other Dissect modules together. It provides a programming API and command line tools which
allow easy access to various data sources inside disk images or file collections (a.k.a. targets).

Installation
------------

``dissect.target`` is available on `PyPI <https://pypi.org/project/dissect.target/>`_.

.. code-block:: console

    $ pip install dissect.target

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This is the "main" package with all the tools as documented on this site. However, you can also interact with it using Python.
For example, to print the hostname, version and all users records:

.. code-block:: python

    from dissect.target import Target

    target = Target.open("/path/to/target")
    print("Hostname:", target.hostname)
    print("Version:", target.version)

    for user in target.users():
        print(user)

The ``Target.open`` function works transparently on all targets for which a supported loader (see :doc:`/advanced/loaders`) exists.

For more advanced examples, please refer to :doc:`/advanced/api`.

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.target`.
