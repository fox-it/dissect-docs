dissect.executable
================

.. button-link:: https://github.com/fox-it/dissect.executable
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for various executable formats such as PE, ELF and Macho-O.
Currently, only ELF is being parsed.

Installation
------------

``dissect.executable`` is available on `PyPI <https://pypi.org/project/dissect.executable/>`_.

.. code-block:: console

    $ pip install dissect.executable

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to open an ELF file
and start reading from it:

.. code-block:: python

    from pathlib import Path
    from dissect.executable.elf import ELF

    elf_file = Path("/path/to/hello_world.out")
    with elf_file.open("rb") as fh:
        elf = ELF(fh)

        for segment in elf.segments:
            print(str(segment))
        
        for section in elf.section_table:
            print(str(section))
        
        for symbol_table in elf.symbol_tables:
            for symbol in symbol_table:
                print(str(symbol))



Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.executable`.
