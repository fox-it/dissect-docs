dissect.fat
===========

.. button-link:: https://github.com/fox-it/dissect.fat
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for the FAT and exFAT file systems, commonly used on flash memory based storage
devices and UEFI partitions.

Installation
------------

``dissect.fat`` is available on `PyPI <https://pypi.org/project/dissect.fat/>`_.

.. code-block:: console

    $ pip install dissect.fat

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.fat import FATFS

    fh = open_fatfs_volume()  # i.e. using dissect.volume

    # Supports FAT12, 16 and 32
    fs = FATFS(fh)
    print(list(fs.get("/").iterdir()))

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.fat`.
