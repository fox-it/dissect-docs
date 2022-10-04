dissect.sql
===========

.. button-link:: https://github.com/fox-it/dissect.sql
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parsers for the SQLite database file format, commonly used by applications to store
configuration data.

Installation
------------

``dissect.sql`` is available on `PyPI <https://pypi.org/project/dissect.sql/>`_.

.. code-block:: console

    $ pip install dissect.sql

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print all
records of all tables of an SQLite database:

.. code-block:: python

    from dissect.sql import SQLite3

    with open("/path/to/file.db", "rb") as fh:
        db = SQLite3(fh)

        for table in db.tables():
            for row in table.rows():
                print(row)


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.sql`.
