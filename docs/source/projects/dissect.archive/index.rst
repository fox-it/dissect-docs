dissect.archive
===============

.. button-link:: https://github.com/fox-it/dissect.archive
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for various archive and backup formats. Currently has support for:
- WIM (Windows Imaging Format)


Installation
------------

``dissect.archive`` is available on `PyPI <https://pypi.org/project/dissect.archive/>`_.

.. code-block:: console

    $ pip install dissect.archive

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file from a WIM archive:

.. code-block:: python

    from dissect.archive.wim import WIM

    fh = open("path/to/file.wim", "rb")

    wim = WIM(fh)
    for image in wim.images():
        print(image.get("/").listdir())

        file_fh = image.get("/file.txt").open()  # This is just another file-like object
        print(file_fh.read())

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.archive`.
