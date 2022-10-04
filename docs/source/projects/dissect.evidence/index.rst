dissect.evidence
================

.. button-link:: https://github.com/fox-it/dissect.evidence
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parsers for various forensic evidence file containers, currently: AD1, ASDF and EWF.

Installation
------------

``dissect.evidence`` is available on `PyPI <https://pypi.org/project/dissect.evidence/>`_.

.. code-block:: console

    $ pip install dissect.evidence

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to open an EWF container
and start reading from it:

.. code-block:: python

    from pathlib import Path
    from dissect.evidence.ewf import EWF, find_files

    e01_file = Path("/path/to/evidence.E01")
    all_files = find_files(e01_file)
    ewf = EWF([f.open() for f in all_files])
    print(ewf.read(512))

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.evidence`.
