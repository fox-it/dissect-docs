dissect.fve
===========

.. button-link:: https://github.com/fox-it/dissect.fve
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for full volume encryption implementations,
currently Microsoft's BitLocker Disk Encryption (BDE) and Linux Unified Key Setup (LUKS1 and LUKS2).

* Full volume and disk encryption schemes

  * Microsoft BitLocker Disk Encryption (all configurations and versions, including EOW): :class:`~dissect.fve.bde.BDE`
  * Linux Unified Key Setup (LUKS1 and LUKS2): :class:`~dissect.fve.luks.LUKS`


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

fve-dd
~~~~~~

The ``fve-dd`` tool is used to decrypt Microsoft BitLocker (BDE) or Linux Unified Key Setup (LUKS1 and LUKS2) volumes
and write the decrypted content to a file.

If the input file is a disk with multiple volumes/partitions, the output file will be a disk image with the same partition layout,
with the encrypted volumes replaced by their decrypted content.
If the input file is a single encrypted volume, the output file will be a raw image of the decrypted volume.

.. sphinx_argparse_cli::
    :module: dissect.fve.tools.dd
    :func: main
    :prog: fve-dd
    :description: Utility to decrypt BitLocker or LUKS volumes and write them to a file.
    :hook:

Examples
^^^^^^^^

**BitLocker or LUKS volumes with passphrase:**

.. code-block:: console

    $ fve-dd encrypted.dd -p "mypassphrase" -o decrypted_volume.dd

**BitLocker volumes with recovery password:**

.. code-block:: console

    $ fve-dd encrypted.dd -r "123456-789012-345678-901234-567890-123456-789012-345678" -o decrypted.dd

**BitLocker volumes with .BEK file:**

BitLocker External Key (BEK) files can be used to unlock BitLocker encrypted volumes.
These files are typically stored on removable media like USB drives.

.. code-block:: console

    $ fve-dd encrypted.dd -f /path/to/recovery_key.BEK -o decrypted.dd

**LUKS volumes with key file:**

LUKS key files contain the encryption key and can be used instead of a passphrase.

.. code-block:: console

    $ fve-dd encrypted.dd -f /path/to/keyfile -o decrypted.dd

**LUKS volumes with specific key slot:**

You can specify which key slot to use when unlocking a LUKS volume:

.. code-block:: console

    $ fve-dd encrypted.dd -f /path/to/keyfile --key-slot 0 -o decrypted.dd

**LUKS volumes with key file offset and size:**

Similar to the ``cryptsetup`` utility, you can specify the offset and size within a key file:

.. code-block:: console

    $ fve-dd encrypted.dd -f /path/to/keyfile --keyfile-offset 512 --keyfile-size 32 -o decrypted.dd

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.fve`.
