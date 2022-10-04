dissect.clfs
============

.. button-link:: https://github.com/fox-it/dissect.clfs
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the CLFS (Common Log File System) file system of Windows.
Currently only supports the persistent variant.

Installation
------------

``dissect.clfs`` is available on `PyPI <https://pypi.org/project/dissect.c;fs/>`_.

.. code-block:: console

    $ pip install dissect.clfs

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print the
logblock headers and associated containers of a given ``.blf`` file:

.. code-block:: python

    from dissect.clfs import blf

    with open("windows/config/DRIVERS{1c2b59ad-c5f5-11eb-bacb-000d3a96488e}.TM.blf", "rb") as fh:
        blf_instance = blf.BLF(fh)

        for base_record in blf_instance.base_records():
            # Parse the base records and print the logblock record headers
            print(base_record.logblock.header)

            for stream in base_record.streams:
                # Print the associated container names
                for blf_container in base_record.containers:

                    # Check if the stream ID is matching the container ID
                    if blf_container.id != stream.lsn_base.Offset.ContainerId:
                        continue

                    # We can encounter the same container ID for the shadow blocks
                    if blf_container.type != stream.type:
                        continue

                    # Invalid LSN (-1)
                    if stream.lsn_base.PhysicalOffset <= 0:
                        continue

                    # Strip the prepended directory to accommodate for dissect FS
                    # %BLF%\DRIVERS{1c2b59ad-c5f5-11eb-bacb-000d3a96488e}.TMContainer00000000000000000001.regtrans-ms
                    print(f"Associated container: {blf_container.name}")

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.clfs`.
