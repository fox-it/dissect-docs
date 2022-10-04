dissect.esedb
=============

.. button-link:: https://github.com/fox-it/dissect.esedb
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for Microsoft's Extensible Storage Engine Database (ESEDB), used for example in
Active Directory, Exchange and Windows Update.

Installation
------------

``dissect.esedb`` is available on `PyPI <https://pypi.org/project/dissect.esedb/>`_.

.. code-block:: console

    $ pip install dissect.esedb

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print all records of
all tables of an ESE database:

.. code-block:: python

    from dissect.esedb import EseDB

    with open("/path/to/ese.db", "rb") as fh:
        db = EseDB(fh)

        for table in db.tables():
            for record in table.get_records():
                print(record)

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.esedb`.
