dissect.database
================

.. button-link:: https://github.com/fox-it/dissect.database
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for various database formats, including:

- Berkeley DB, used for older RPM databases
- Microsoft Extensible Storage Engine (ESE), used for example in Active Directory, Exchange and Windows Update
- SQLite3, commonly used by applications to store configuration data

Installation
------------

``dissect.database`` is available on `PyPI <https://pypi.org/project/dissect.database/>`_.

.. code-block:: console

    $ pip install dissect.database

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python.
For example, to print all records of all tables of an SQLite database:

.. code-block:: python

    from dissect.database.sqlite3 import SQLite3

    with open("/path/to/file.db", "rb") as fh:
        db = SQLite3(fh)

        for table in db.tables():
            for row in table.rows():
                print(row)

Or to print all records of all tables of an ESE database:

.. code-block:: python

    from dissect.database.ese import ESE

    with open("/path/to/ese.db", "rb") as fh:
        db = ESE(fh)

        for table in db.tables():
            for record in table.get_records():
                print(record)


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.database`.

