dissect.btrfs
=============

.. button-link:: https://github.com/fox-it/dissect.btrfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the Btrfs file system, a commonly used Linux filesystem.

Installation
------------

``dissect.btrfs`` is available on `PyPI <https://pypi.org/project/dissect.btrfs/>`_.

.. code-block:: console

    $ pip install dissect.btrfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.btrfs import Btrfs

    fh = open_btrfs_volume()  # i.e. using dissect.volume

    fs = Btrfs(fh)
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.btrfs`.
