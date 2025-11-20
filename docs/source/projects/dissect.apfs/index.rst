dissect.apfs
============

.. button-link:: https://github.com/fox-it/dissect.apfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for the APFS file system, a commonly used Apple file system.

Installation
------------

``dissect.apfs`` is available on `PyPI <https://pypi.org/project/dissect.apfs/>`_.

.. code-block:: console

    $ pip install dissect.apfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tool, so you can only interact with it from Python.
For example, to print a directory listing of the root directory and read a file:

.. code-block:: python

    from dissect.apfs import APFS

    with open("path/to/apfs/file", "rb") as fh:
        apfs = APFS(fh)

        volume = apfs.volume[0]
        print(volume.get("/").listdir())


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.apfs`.
