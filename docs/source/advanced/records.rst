Working with Records
====================

This section describes how to work with records. Records are the fundamental data structure in ``dissect`` and are
used to describe forensic evidence and artefacts in a structured way. They can be read from and written to various
sources and formats.

Writing Records with rdump
--------------------------

The easiest way to write records is by using the :doc:`/tools/rdump` tool. It allows you to read records from any
source, filter them, and write them to a new destination.

The output format is determined by the ``-w/--writer`` argument. You can specify a filename, and ``rdump`` will
automatically detect the desired output format and compression based on the file extension.

For example, to write records to a gzip-compressed file, you can use:

.. code-block:: console

    $ rdump <source> -w output.rec.gz

Writing Records with Python
---------------------------

For more advanced use-cases, you can use the :class:`flow.record.RecordWriter` class in your own Python scripts. This
gives you full control over how and where records are written.

The ``RecordWriter`` is best used as a context manager. It takes a URI as its main argument, which specifies the
adapter and any options to use.

Here's an example of writing records to a JSON file:

.. code-block:: python

    from flow.record import RecordWriter, Record

    records = [
        Record(myfield="value1"),
        Record(myfield="value2"),
    ]

    with RecordWriter("jsonfile://output.json?indent=2") as writer:
        for record in records:
            writer.write(record)

Adapters
--------

The ``RecordWriter`` uses adapters to write to different formats. The adapter is selected based on the scheme of the
URI passed to the ``RecordWriter``.

Some common adapters include:

* ``file``: The default record stream format.
* ``csvfile``: For writing CSV files.
* ``jsonfile``: For writing JSON or JSONL files.
* ``line``: For writing to the console in a human-readable format.

You can get a full list of available adapters by running ``rdump --list-adapters``.

.. seealso::

    For more information about the ``flow.record`` library, please refer to the :doc:`/projects/flow.record/index` page.
