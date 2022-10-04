dissect.vmfs
============

.. button-link:: https://github.com/fox-it/dissect.vmfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the VMFS file system, used by VMware virtualization software.

Installation
------------

``dissect.vmfs`` is available on `PyPI <https://pypi.org/project/dissect.vmfs/>`_.

.. code-block:: console

    $ pip install dissect.vmfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print a directory
listing of the root directory and read a file:

.. code-block:: python

    from dissect.vmfs import LVM, VMFS

    fh = open_vmfs_volume()  # i.e. using dissect.volume

    lvm = LVM([fh])  # First open a VMFS LVM on one or more disks
    fs = VMFS(lvm)  # Then open the filesystem on the LVM
    print(fs.get("/").listdir())

    file_fh = fs.get("/file.txt").open()  # This is just another file-like object
    print(file_fh.read())


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.vmfs`.
