dissect.etl
===========

.. button-link:: https://github.com/fox-it/dissect.etl
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for Event Trace Log (ETL) files, used by the Windows operating system to log
kernel events.

Installation
------------

``dissect.etl`` is available on `PyPI <https://pypi.org/project/dissect.etl/>`_.

.. code-block:: console

    $ pip install dissect.etl

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print all
records in an ETL file:

.. code-block:: python

    from dissect.etl import ETL

    with open("/path/to/file.etl", "rb") as fh:
        etl = ETL(fh)
        for record in etl:
            print(etl)

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.etl`.
