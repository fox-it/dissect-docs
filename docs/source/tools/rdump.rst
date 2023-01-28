rdump
=====

With ``rdump`` you can read, write, interact, and manipulate records from ``stdin`` or from record files saved on disk.

.. hint::

    Don't know yet what a record is? Read more :ref:`here <overview/index:records>` for a detailed explanation.

Records are the primary output type when using the various functions of :doc:`/tools/target-query`.
Keep in mind that not all functions in ``target-query`` output records.

You can check the output type of a function by using ``target-query -l`` and searching for your function.
The output type is specified on the end, and looks something like this:

.. code-block::
    :class: no-copybutton

    runkeys - Iterate various run key locations. See source for all locations. (output: records)
                                                                               ^^^^^^^^^^^^^^^^^

If the output type is ``records`` you can use ``rdump``!

Basic usage
-----------

Since ``target-query`` primarily outputs records it is often used in conjunction with ``rdump``.
Common usage is to pipe the record output from ``target-query`` into ``rdump``:

.. code-block:: console

    $ target-query -f runkeys targets/EXAMPLE.vmx | rdump
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2022-12-09 12:06:20.037806+00:00 name='OneDriveSetup' path='C:/Windows/SysWOW64/OneDriveSetup.exe /thfirstsetup' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='C:\\Windows/ServiceProfiles/LocalService/ntuser.dat' username='LocalService' user_sid='S-1-5-19' user_home='%systemroot%\\ServiceProfiles\\LocalService'>
    <...>

By default, records will be serialized into a binary format when piped to a different command or file so that they
can be deserialized and consumed by another command. This is how ``rdump`` interacts with the records from
``target-query``.

Without specifying any arguments to ``rdump`` the resulting output will be grep-able text.
**NOTE:** The same can be achieved by passing ``target-query`` the ``-s`` flag, so it's recommended you use that if
that is all you want.

You can use ``rdump`` on (multiple) files as well. Just point ``rdump`` to the record file(s) in question:

.. code-block:: console

    $ target-query -f runkeys targets/EXAMPLE.vmx > runkeys.rec
    $ target-query -f services targets/EXAMPLE.vmx > services.rec
    $ rdump runkeys.rec
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2022-12-09 12:06:20.037806+00:00 name='OneDriveSetup' path='C:/Windows/SysWOW64/OneDriveSetup.exe /thfirstsetup' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='C:\\Windows/ServiceProfiles/LocalService/ntuser.dat' username='LocalService' user_sid='S-1-5-19' user_home='%systemroot%\\ServiceProfiles\\LocalService'>
    [...]
    $ rdump *.rec
    <windows/service hostname='EXAMPLE' domain='EXAMPLE.local' ts=2016-11-21 08:06:04.528015 name='Wof' displayname='Windows Overlay File System Filter Driver' servicedll=None imagepath=None imagepath_args=None objectname=None start='Boot (0)' type='File System Driver (0x2)' errorcontrol='Normal (1)'>
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2022-12-09 12:06:20.037806+00:00 name='OneDriveSetup' path='C:/Windows/SysWOW64/OneDriveSetup.exe /thfirstsetup' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='C:\\Windows/ServiceProfiles/LocalService/ntuser.dat' username='LocalService' user_sid='S-1-5-19' user_home='%systemroot%\\ServiceProfiles\\LocalService'>
    [...]

The file extension of the record file can be anything you want.

Timeline & datetime fields
--------------------------

``target-query`` functions that have a ``record`` with the fieldtype ``datetime`` are outputed in a single record. As shown below with the function ``mft``:

.. code-block:: console

    $ target-query -f mft -t targets/EXAMPLE.tar --limit 1 | rdump
    <filesystem/ntfs/mft/std hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411+00:00 last_modification_time=2019-03-19 21:52:25.169411+00:00 last_change_time=2019-03-19 21:52:25.169411+00:00 last_access_time=2019-03-19 21:52:25.169411+00:00 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>

The single record contains four different events that occured on the filesystem:

* ``creation_time``
* ``last_modification_time``
* ``last_change_time``
* ``last_access_time``

To analyze a timeline of events that occured every record needs a single ``datetime`` field on which can be filtered to view records in chronological order.

For this purpose the argument ``--multi-timestamp`` can be used to output multiple ``ts`` enriched records based on the ``datetime`` fields of the original record.

.. code-block:: console

    $ target-query -f mft -t targets/EXAMPLE.tar --limit 1 | rdump --multi-timestamp
    [reading from stdin]
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='creation_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_modification_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_change_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_access_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>

Filtering & manipulating records
--------------------------------

One of the things you can do with ``rdump`` is filtering records. This can be done with the ``-s`` or ``--selector``
argument. This argument takes a Python statement which must evaluate to ``True`` or ``False``. This statement is used
to filter records. You can interact with the fields of a record using the magic ``r`` variable.

.. code-block:: console

    $ rdump services.rec -s '"%systemroot%" not in r.imagepath.lower()'
    <windows/service hostname='EXAMPLE' domain='EXAMPLE.local' ts=2021-06-01 12:55:07.103594 name='ACPI' displayname='@acpi.inf,%ACPI.SvcDesc%;Microsoft ACPI Driver' servicedll=None imagepath='System32/drivers/ACPI.sys' imagepath_args='' objectname=None start='Boot (0)' type='Kernel Device Driver (0x1)' errorcontrol='Critical (3)'>
    [...]

To manipulate the output generated by ``rdump`` the ``-f (--format)`` and ``-F (--fields)`` arguments can be used.
The ``-f`` behaves as a Python format-string, record fields can be referred to by their field name in braces (e.g. ``{path}``).
For example, we can output just the hostname, name and image path of a Windows service:

.. code-block:: console

    $ rdump services.rec -f '{hostname} - {name}:{imagepath}'
    EXAMPLE - 1394ohci:/SystemRoot/System32/drivers/1394ohci.sys
    EXAMPLE - 3ware:System32/drivers/3ware.sys
    EXAMPLE - ACPI:System32/drivers/ACPI.sys
    EXAMPLE - AcpiDev:/SystemRoot/System32/drivers/AcpiDev.sys
    [...]

.. seealso::

    Please refer to :doc:`/usage/use-cases` for more examples of how to use ``rdump``.

Writing records
---------------

Something about writing records, e.g. auto detection of filename for compression.

Usage
-----

.. sphinx_argparse_cli::
    :module: flow.record.tools.rdump
    :func: main
    :prog: rdump
    :hook:
