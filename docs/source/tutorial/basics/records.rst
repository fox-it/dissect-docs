Records
=======

Many Dissect tools generate so-called "records" as their output rather than text or json.

In this section you will learn what records are on a conceptual level and how you can output, search,
store, retreive and convert them using Dissect tools.

Basic commands will be shown to export records to popular tools such as Splunk and Elasticsearch,
but this will be explained in more detail later in the tutorial.

What are records?
-----------------

Records are a simple, uniformly structured and versatile key/value storage format created by Fox-IT. You can think of it as JSON, but strongly
typed. By making the keys strongly typed, Dissect knows how to interpret the data contained in the records;
something you miss when just using JSON or text output.

Records were invented because:
- solve problem 1
- 2
- 3

For example, where a JSON output may consist of ``"source_ip": "192.168.1.1"``, it is difficult to check - based on the
textual representation of the IP address, if it is in the subnet ``192.0.0.0/8``. For records, FIXME VOORBEELD AFMAKEN

When a records is printed on screen, it has the following form:

.. code-block:: console

    <record/type/name key1=value1, key2=value2, ... >

Each record:

    - starts with a ``<`` and end with ``>``
    - Each record has a *record type*, in this case ``record/type/name``
    - Each record has various ``keys`` and their corresponding values

.. note::

    The ``keys`` of a record are also called ``fields``. These terms can be used interchangeably.

Depending on the type of information contained in a record, it will have a different record type and corresponding fields.
In <Examples> you will see different examples of records as they are used in Dissect.


How are records created?
------------------------

Dissect tools such as ``target-query`` (see :ref:`/tutorial/basics/targets`) can output records.

The ``rdump`` tool (:doc:`/tools/rdump`) can be used to convert, search, read and write records in multiple ways.

Examples of records
-------------------

In the following examples, we use ``target-query`` on a target set up in :doc:`/tutorial/preparation` and on your own
computer. You will see how this command outputs different record types.

MFT records
^^^^^^^^^^^

Dissect can be used to list all ``MFT entries <https://en.wikipedia.org/wiki/NTFS#Master_File_Table>``
of a target.

Issue the command below in your working environment (you can use ``ctrl-c`` to stop the command as your screen will
fill quickly with the output):

.. code-block:: console

    $ target-query -f mft t/SCHARDT.001
    <filesystem/ntfs/mft/std hostname='N-1A9ODN6ZXK4LQ' domain=None ts=2004-08-19 16:57:43.694986+00:00 ts_type='B' segment=0 path='c:/$MFT' owner='S-1-5-32-544' filesize=12.0 MB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std hostname='N-1A9ODN6ZXK4LQ' domain=None ts=2004-08-19 16:57:43.694986+00:00 ts_type='C' segment=0 path='c:/$MFT' owner='S-1-5-32-544' filesize=12.0 MB resident=False inuse=True volume_uuid=None>
    [...]

Each line in the output represents a record and each record represents one MFT entry of our target ``SCHARDT.001``.
Let's break down the output of a single line:

.. FIXME Records and Target in deze tutroial caps?

- ``<>`` records start with a ``<`` and end with ``>``
- Each record has the record type ``filesystem/ntfs/mft/std``
- Each record has various ``fields`` containing information related to MFT entriess.

.. note::
    When ``target-query`` outputs records to at TTY device such as a terminal, the output is automatically converted to text. However, when
    outputting the records to other tools, they are 'pure' records.


Browser history records
^^^^^^^^^^^^^^^^^^^^^^^

To see another example of records and indeed a usecase of ``target-query``, we can try and get all FireFox and Chrome browser history entries of a system.
If you have either browser running on your system, try these commands:

.. code-block:: console

    $ target-query -f firefox.history,chrome.history /
    <browser/firefox/history hostname='ubuntu' domain=None ts=xxxx browser='firefox' id='x' url='https://www.google.com/' (...)>

You will see similar output as in the previous example, but now the recored types are
``browser/firefox/history`` or ``browser/chrome/history``.
Again, they also contain different ``fields``, namely those that represent browser history items such as a url, how many times
a url was visited, and a timestamp of the last visit.

You have now seen two examples of records and what they look like. In the next sections you will
learn how to use the tool ``rdump`` to manipulate records so you can start your forensic analysis!




Takeaways
~~~~~~~~~

The most important takeaways of this section are:

1. Records is a format to store and transfer information efficiently
2. Records are the main output of ``target-query``
3. Records can be manipulated using the ``rdump`` tool
4. Records can be converted to many different formats
5. Records can be sent to many other 3rd party analysis tools.

meaning that the information contained


For example, we may define a record as having a timestamp field of type ``datetime``, or an IP address field
of type ``net.ipaddress``. You can interact with specific attributes of these fields, too. For example, you can get the
``filename`` attribute of an ``uri`` field to just get the filename of that path.