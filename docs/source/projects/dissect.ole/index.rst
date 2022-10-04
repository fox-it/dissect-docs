dissect.ole
===============

.. button-link:: https://github.com/fox-it/dissect.ole
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the Object Linking & Embedding (OLE) format, commonly used by document
editors on Windows operating systems.

Note: this module is currently not actively used. Functionality is limited and it may change significantly in the future.

Installation
------------

``dissect.ole`` is available on `PyPI <https://pypi.org/project/dissect.ole/>`_.

.. code-block:: console

    $ pip install dissect.ole

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python.

.. code-block:: python

    from dissect.ole import OLE

    with open("/path/to/ole/file", "rb") as fh:
        obj = OLE(fh)
        print(obj.listdir())


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.ole`.
