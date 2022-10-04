dissect.util
============

.. button-link:: https://github.com/fox-it/dissect.util
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing various utility functions for the other Dissect modules.

* Compression algorithms (:mod:`dissect.util.compression`)
* ``NSKeyedArchiver`` plist implementation (:mod:`dissect.util.plist`)
* Windows SID parser (:mod:`dissect.util.sid`)
* Stream implementations and helpers (:mod:`dissect.util.stream`)
* Timestamp parsers and helpers (:mod:`dissect.util.ts`)

Installation
------------

``dissect.util`` is available on `PyPI <https://pypi.org/project/dissect.util/>`_.

.. code-block:: console

    $ pip install dissect.util

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with a few CLI tools, so you primarily interact with it from Python. Most of the functionality
of this library should be pretty straightforward from the API documentation, so here's an example on how to implement
your own :class:`~dissect.util.stream.AlignedStream`:

.. code-block:: python

    from typing import BinaryIO

    from dissect.util.stream import AlignedStream


    class MyStream(AlignedStream):
        def __init__(self, fh: BinaryIO, size: int):
            # Customize the __init__ however you need
            self.fh = fh
            # You only need to give the super class the size (and optional ``align``)
            super().__init__(size)

        def _read(self, offset: int, length: int):
            # This is the only method you have to implement
            # Do whatever you need to do to return ``length`` amount of bytes (or less if EOF)
            self.fh.seek(offset)
            return self.fh.read(length)

Tools
-----

.. sphinx_argparse_cli::
    :module: dissect.util.tools.dump_nskeyedarchiver
    :func: main
    :prog: dump-nskeyedarchiver
    :description: Utility to dump NSKeyedArchiver plist files.
    :hook:


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.util`.
