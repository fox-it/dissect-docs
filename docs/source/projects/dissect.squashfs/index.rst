dissect.squashfs
================

.. button-link:: https://github.com/fox-it/dissect.squashfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the SquashFS file system, commonly used in appliance or device firmware.

Installation
------------

``dissect.squashfs`` is available on `PyPI <https://pypi.org/project/dissect.squashfs/>`_.

.. code-block:: console

    $ pip install dissect.squashfs

This project decompresses lzo and lz4 compressed file systems and can use the faster, native (C-based) lzo and lz4
implementations when installed, instead of the slower pure Python implementation provided by
:doc:`/projects/dissect.util/index`. To use these faster implementations, install the package with the lzo and lz4
extras:

   .. code-block:: console

    $ pip install "dissect.squashfs[lz4,lzo]"

Unfortunately there is no binary ``python-lzo`` wheel for PyPy installations on Windows, so it won't be installed there.

This module including the lz4 and lzo extras is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.squashfs import SquashFS

    fh = open_squashfs_volume_or_file()  # i.e. using dissect.volume or open(path, "rb")

    fs = SquashFS(fh)
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.squashfs`.
