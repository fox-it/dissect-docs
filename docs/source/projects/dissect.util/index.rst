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

``dissect.util`` includes both a pure Python implementation as well as a faster native Rust implementation of the LZ4 and LZO decompression algorithms.
Pre-build wheels are available for most common platforms and the native implementation will automatically be used.
In the rare case that a pre-build wheel is not available, the pure Python implementation will automatically be used instead.
If you wish to build your own wheel in the case a pre-build one is not available for your platform, you can do so by running the following command:

.. code-block:: console

    $ tox -e build-native

Note that you'll need to bring your own Rust toolchain for the target platform you wish to build a wheel for. For example, using [rustup](https://rustup.rs).

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
