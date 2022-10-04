flow.record
===========

.. button-link:: https://github.com/fox-it/flow.record
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A library for defining and creating structured data (called records) that can be streamed to disk or piped to other
tools that use flow.record.

Records can be read and transformed to other formats by using output adapters, such as CSV and JSON.

Installation
------------

``flow.record`` is available on `PyPI <https://pypi.org/project/flow.record/>`_.

.. code-block:: console

    $ pip install flow.record

Usage
-----

This library contains the tool ``rdump``. With ``rdump`` you can read, write, interact, and manipulate records from ``stdin``
or from record files saved on disk. Please refer to ``rdump -h`` or to the :doc:`rdump documentation </tools/rdump>` for all parameters.

Records are the primary output type when using the various functions of ``target-query``. The following command shows how
to pipe record output from ``target-query`` to ``rdump``:

.. code-block:: console

    $ target-query -f runkeys targets/EXAMPLE.vmx | rdump
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2022-12-09 12:06:20.037806+00:00 name='OneDriveSetup' path='C:/Windows/SysWOW64/OneDriveSetup.exe /thfirstsetup' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='C:\\Windows/ServiceProfiles/LocalService/ntuser.dat' username='LocalService' user_sid='S-1-5-19' user_home='%systemroot%\\ServiceProfiles\\LocalService'>
    <...>


Programming example
~~~~~~~~~~~~~~~~~~~

Define a ``RecordDescriptor`` (schema) and then create a few records and write them to disk

.. code-block:: python

    from flow.record import RecordDescriptor, RecordWriter

    # define our descriptor
    MyRecord = RecordDescriptor("my/record", [
        ("net.ipaddress", "ip"),
        ("string", "description"),
    ])

    # define some records
    records = [
        MyRecord("1.1.1.1", "cloudflare dns"),
        MyRecord("8.8.8.8", "google dns"),
    ]

    # write the records to disk
    with RecordWriter("output.records.gz") as writer:
        for record in records:
            writer.write(record)

The records can then be read from disk using the ``rdump`` tool or by instantiating a ``RecordReader`` when using the
library.

.. code-block:: console

    $ rdump output.records.gz
    <my/record ip=net.ipaddress('1.1.1.1') description='cloudflare dns'>
    <my/record ip=net.ipaddress('8.8.8.8') description='google dns'>

Selectors
~~~~~~~~~

We can also use ``selectors`` for filtering and selecting records using a query (Python like syntax), e.g.:

.. code-block:: console

    $ rdump output.records.gz -s '"google" in r.description'
    <my/record ip=net.ipaddress('8.8.8.8') description='google dns'>

    $ rdump output.records.gz -s 'r.ip in net.ipnetwork("1.1.0.0/16")'
    <my/record ip=net.ipaddress('1.1.1.1') description='cloudflare dns'>

Reference
---------

For more details, please refer to the API documentation of :mod:`flow.record`.
