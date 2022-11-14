dissect.thumbcache
==================

.. button-link:: https://github.com/fox-it/dissect.thumbcache
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for the thumbcache of Windows systems.
This is commonly used to see which files were opened on a system.

Installation
------------

``dissect.thumbcache`` is available on `PyPI <https://pypi.org/project/dissect.thumbcache/>`_.

.. code-block:: console

    $ pip install dissect.thumbcache

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with a few CLI tools, so you primarily interact with it from Python.
For example, to access thumbnail entries from ``thumbnail_*.db`` files:

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
    
Tools
-----

.. sphinx_argparse_cli::
    :module: dissect.thumbcache.tools.extract_images
    :func: main
    :prog: thumbcache-extract
    :hook:

.. sphinx_argparse_cli::
    :module: dissect.thumbcache.tools.extract_with_index
    :func: main
    :prog: thumbcache-extract-indexed
    :hook:

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.thumbcache`.
