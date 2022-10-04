dissect.extfs
=============

.. button-link:: https://github.com/fox-it/dissect.extfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the ExtFS file system, the native filesystem for Linux operating systems.

Installation
------------

``dissect.extfs`` is available on `PyPI <https://pypi.org/project/dissect.extfs/>`_.

.. code-block:: console

    $ pip install dissect.extfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.extfs import ExtFS

    fh = open_ext4_volume()  # i.e. using dissect.volume

    fs = ExtFS(fh)
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.extfs`.
