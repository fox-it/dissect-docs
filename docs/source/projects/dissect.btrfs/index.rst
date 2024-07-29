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

This project decompresses lzo compressed file systems and can use the faster, native (C-based) lzo implementation when
installed, instead of the slower pure Python implementation provided by :doc:`/projects/dissect.util/index`. To use
these faster implementations, install the package with the lzo extra:

   .. code-block:: console

    $ pip install "dissect.btrfs[lzo]"

Unfortunately there is no binary ``python-lzo`` wheel for PyPy installations on Windows, so it won't be installed there.

This module including the lzo extra is also automatically installed if you install the ``dissect`` package.

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
