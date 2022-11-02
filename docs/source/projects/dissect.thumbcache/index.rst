dissect.thumbcache
==================

.. button-link:: https://github.com/fox-it/dissect.thumbcache
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parsers for the windows Thumbcache file format.
This format gets used to store thumbnail information.
Interestingly, the last entry inside a thumbcache file contains random data.
This entry is often unused, however the data could be anything that was on that specific space on disk first.

Installation
------------

``dissect.thumbcache`` is available on `PyPI <https://pypi.org/project/dissect.thumbcache/>`_.

.. code-block:: console

    $ pip install dissect.thumbcache

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This pacakge is a library which you can use to extract thumbnail images from ``thumbnail_*.idx``.

.. sphinx_argparse_cli::
    :module: dissect.thumbcache.tools.extract_images
    :func: main
    :prog: thumbcache-extract
    :hook:

.. sphinx_argparse_cli::
    :module: dissect.thumbcache.tools.extract_images_indexed
    :func: main
    :prog: thumbcache-extract-indexed
    :hook:

Additionally, you can get the entries of a file programatically using:

.. code-block:: python

    from dissect.thumbcache import ThumbcacheFile

    path = Path("path/to/thumbcache_file.db")

    with path.open("rb") as file:
        cache_file = ThumbcacheFile(file)
        entries = cache_file.entries()

Or only the indexed entries:

.. code-block:: python

    from dissect.thumbcache import Thumbcache

    path = Path("path/to/thumbcache_files/")

    cache = Thumbcache(path=path)
    entries = list(cache.entries())


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.thumbcache`.