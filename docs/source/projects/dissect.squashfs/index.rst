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

This project supports file systems with LZO and LZ4 compression. It can use either a fast Rust implementation, or a slow pure Python implementation. Both implementations are provided by :doc:`/projects/dissect.util/index`, and the faster implementation will automatically be used if available.
Pre-build wheels are available for most common platforms. In the rare case that a pre-build wheel is not available, please refer to :doc:`/projects/dissect.util/index` for build instructions.
Pre-build wheels are available for most common platforms and the native implementation will automatically be used if available.
In the rare case that a pre-build wheel is not available, please refer to :doc:`/projects/dissect.util/index` for build instructions.

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
