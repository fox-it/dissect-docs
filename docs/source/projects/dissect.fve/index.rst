dissect.fve
============

.. button-link:: https://github.com/fox-it/dissect.fve
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for full volume encryption implementations, 
currently Microsoft's Bitlocker Disk Encryption (BDE) and Linux Unified Key Setup (LUKS1 and LUKS2).

* Full volume and disk encryption schemes

   * BDE (BitLocker disk encryption) (:class:`~dissect.fve.bde.BDE`)
   * LUKS (Linux Unified Key Setup) (:class:`~dissect.fve.luks.LUKS`)


Installation
------------

``dissect.fve`` is available on `PyPI <https://pypi.org/project/dissect.fve/>`_.

.. code-block:: console

    $ pip install dissect.fve

This module is also automatically installed if you install the ``dissect`` package.


Usage
-----

This package is a library with a CLI tool, so you primarily interact with it from Python. For example, 
to open and decrypt a BitLocker encrypted volume for reading:

.. code-block:: python

    from dissect.fve import BDE
    from dissect.ntfs import NTFS

    with open("path/to/bitlocker/file.dd", "rb") as fh:
        bde = BDE(fh)
        bde.unlock_with_passphrase("kusjesvansrt<3")
        
        fs = NTFS(bde.open())
        print(fs.get("/").listdir())

        file_fh = fs.get("/file.txt").open()  # This is just another file-like object
        print(file_fh.read())

Tools
-----
.. sphinx_argparse_cli::
    :module: dissect.fve.tools.dd
    :func: main
    :prog: fve-dd
    :description: Utility to decrypt BitLocker or LUKS volumes and write them to a file.
    :hook:


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.fve`.
