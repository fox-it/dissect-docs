Don't worry if you cannot remember all examples straightaway as there will be plenty of examples in the rest of the tutorial.

Using rdump to format output
----------------------------

We saw in the example above that querying the MFT table for SCHARDT.001 resulted in many records with
a lot of fields, some of which we may not be interested in. Using ``rdump`` we can filter the output
of the records to show only the fields that we want to see.

You can use the ``-F`` function of ``rdump`` to specify a comma separated list of keys of records
that you want to output, like so:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path,



NOTE WHOAH ZIE JE WAT ER GEBEURT ONDERWATER WE HEBBEN HELEMAAL NIET NAGEDACHT OVER MOUNTEN OF UNPACKEN  ALLES ZAT IN DISSECT

Using rdump to search for items
-------------------------------

When you want to search for records with specific values, there are some simple ways to do that with ``rdump``.

Suppose you want to find all DLL files (files ending with '.dll') installed on the system above. You can use the output of ``rdump`` and ``grep`` to
find information you need as such:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path | grep -i dll

When you inspect the output of that command, you certainly get a lot of DLL files, but also files that have DLL in the name
such as ``RUNDLL32.exe``.

Using the power of so-called *selectors*, you can create very powerful search queries within ``rdump`` to
select only the records that you need.

Here is an example of using a selector; you will find the syntax to be self-explanatory if you have familiarity with Python:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -s "r.path.filename.lower().endswith('.dll')" -F path

As you can see, specifying the selector to ``rdump`` selects only those records that match the query.

.. note::

    Unlike when using the ``-F`` and ``-f`` flags, the selector syntax requires you to start
    your expression with ``r.``.


Selector syntax
---------------

The selector syntax used above is executed in a Python context and hence should be easy to learn. If you know what
type a key is in your record, you can use Python methods in your expressions.



DATE Example
IP ADRESS




FIXME: hoe kan je achterhalen welke attributen?



Using rdump to output records in json, CSV, etc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use the ``-m`` option of ``rdump`` to specify the output mode. There are options
to output to json, CSV and more (see also ``rdump -h``).

For json output there is the shorthand ``-j``, for other output types use ``-m``.

FIXME json eenduidig hoofdletters of niet


To show the output of records as JSON:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path -j

or equivalently:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path -m json

To show the output of records as CSV:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path -m csv

You can combine this with the ``-f`` and ``-s`` flags as above as in the example below:

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -F path -j -s "r.path.filename.lower().endswith('.dll')"
    {
      "path": "c:/Program Files/Common Files/SYSTEM/ADO/msado15.dll",
      "_source": "/mnt/t/SCHARDT.001",
      "_classification": null,
      "_generated": "2023-04-26T11:45:05.960914",
      "_version": 1
    }

FIXME IETS OVER SOURCE/CLASS


Using ``rdump`` to read and write records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use ``rdump`` to read and write records in files for later use. For example, the generating MFT records
from a disk image may take a fairly long time. If you have multiple queries on these MFT records, it is best to
write them to a separate file first and then query them by reading that file. This will save a lot of processing time!

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001 | rdump -w dllfiles.records -s "r.path.filename.lower().endswith('.dll')"

In the example above, we use ``target-query`` to once again find all DLL files on the disk. But instead of outputting
the results directly, we use the ``-w`` flag to write the records into ``dllfiles.records``. Afterwards, you will have
a file with records which is a fraction of the size of the disk image:

.. code-block:: console

    $ ls -lh dllfiles.records

The reported filesize should probably be around the 4 megabytes.

With this file, you can now do subsequent analysis such as below:

.. code-block:: console

    $ rdump dllfiles.records -F path -s "'/WINDOWS/' in r.path"

This outputs all DLL files from our ``dllfiles.records`` in our file which are located in a path which contains '/WINDOWS/'.

You can use the special ``-`` character for the ``-w`` flag to indicate that you want to write the records to stdout. This
can be useful if you want to use the output of ``rdump`` in other tools that accept records.


Using ``rdump`` to send records to Splunk, Elastic, etc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to writing records to a file, ``rdump`` can also write



Using ``rdump`` to send records to Elastic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to writing records to a file, ``rdump`` can also write



