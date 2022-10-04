dissect.volume
==============

.. button-link:: https://github.com/fox-it/dissect.volume
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for different disk volume and partition systems, for example LVM2, GPT and MBR.

Installation
------------

``dissect.volume`` is available on `PyPI <https://pypi.org/project/dissect.volume/>`_.

.. code-block:: console

    $ pip install dissect.volume

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print
all partitions on a disk:

.. code-block:: python

    from dissect.volume.disk import Disk

    fh = open_disk()  # Open any disk as a file-like object, e.g. a virtual disk using dissect.hypervisor

    disk = Disk(fh)
    print(disk.partitions)


Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.volume`.
