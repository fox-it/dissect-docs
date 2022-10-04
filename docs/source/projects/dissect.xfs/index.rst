dissect.xfs
===========

.. button-link:: https://github.com/fox-it/dissect.xfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the XFS file system, commonly used by RedHat Linux distributions.

Installation
------------

``dissect.xfs`` is available on `PyPI <https://pypi.org/project/dissect.xfs/>`_.

.. code-block:: console

    $ pip install dissect.xfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.xfs import XFS

    fh = open_xfs_volume()  # i.e. using dissect.volume

    fs = XFS(fh)
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.xfs`.
