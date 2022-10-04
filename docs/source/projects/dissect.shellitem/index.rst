dissect.shellitem
=================

.. button-link:: https://github.com/fox-it/dissect.shellitem
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the Shellitem structures, commonly used by Microsoft Windows.

Installation
------------

``dissect.shellitem`` is available on `PyPI <https://pypi.org/project/dissect.shellitem/>`_.

.. code-block:: console

    $ pip install dissect.shellitem

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with a few CLI tools, so you primarily interact with it from Python. For example, to open a
LNK file for parsing:

.. code-block:: python

    from dissect.shellitem.lnk import Lnk

    with open("/path/to/file.lnk", "rb") as fh:
        lnk = Lnk(fh)

        # Print the string representation of the parsed LNK file to see available fields
        print(lnk)

Tools
-----

.. sphinx_argparse_cli::
    :module: dissect.shellitem.tools.lnk
    :func: main
    :prog: parse-lnk
    :description: Utility to parse LNK files.
    :hook:


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.shellitem`.
