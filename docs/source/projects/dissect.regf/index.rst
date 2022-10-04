dissect.regf
============

.. button-link:: https://github.com/fox-it/dissect.regf
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for Windows registry file format, used to store application and OS configuration
on Windows operating systems.

Installation
------------

``dissect.regf`` is available on `PyPI <https://pypi.org/project/dissect.regf/>`_.

.. code-block:: console

    $ pip install dissect.regf

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print the
subkeys from the root of a hive:

.. code-block:: python

    from dissect.regf import RegistryHive

    with open("/path/to/SYSTEM", "rb") as fh
        hive = RegistryHive(fh)
        for subkey in hive.root.subkeys():
            print(subkey)


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.regf`.
