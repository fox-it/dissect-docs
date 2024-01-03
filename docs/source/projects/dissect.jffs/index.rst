dissect.jffs
============

.. button-link:: https://github.com/fox-it/dissect.jffs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the JFFS2 file system, commonly used by router operating systems.

Installation
------------

``dissect.jffs`` is available on `PyPI <https://pypi.org/project/dissect.jffs/>`_.

.. code-block:: console

    $ pip install dissect.jffs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.jffs.jffs2 import JFFS2

    fh = open_jffs_volume()  # i.e. using dissect.volume

    fs = JFFS2(fh)
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.jffs`.
