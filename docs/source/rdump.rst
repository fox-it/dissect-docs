rdump
-----

By default, target-query generates records. Records in this sense are binary representations of parsed artefacts.
They are transformed to text by the default mechanism. An example is given below:

.. code-block:: console

    <record key1="value1" key2="value2" >

With ``rdump`` you can transform the stream of records to your liking. The ``rdump`` utility allows you to:

* Select certain fields from the records.
* Filter certain records.
* Create additional derived fields.
* Limit the output.
* Format the results.
* Write the results through an adapter.

.. hint::

    Don't know yet what a record is? Read more :ref:`here <overview/index:records>` for a detailed explanation.

Field Selection
~~~~~~~~~~~~~~~

Imagine we're going to extract a list of users from a forensic image using:

.. code-block:: console

    $ target-query host.img -f users 

To select only the name and home fields we use the ``-F`` option:

.. code-block:: console

    $ target-query host.img -f users | rdump -F name,home

Using the ``-X`` option we can exclude fields:

    $ target-query host.img -f users | rdump -X hostname,domain,sid


Filtering
~~~~~~~~~

Filtering records can be done through the ``-s`` option.
The selection option must be a Python-expression, where the record is represented with the symbol ``r``.
So to eliminate all records that for example have no domain value:

.. code-block:: console

    $ target-query host.img -f users | rdump -F name,home -s "r.domain is not None"


Derivations
~~~~~~~~~~~

It is possible to create new fields derived from other fields. This can be done by using
an expression and the ``-E`` option. The following example lists all dll files from
a host and adds the filename to a separate field:

.. code-block:: console

    $ target-query host.img -f walkfs | rdump -s "r.path.suffix=='.dll'" -F path,file,size -E "file=path.name"
    
    <filesystem/entry path='\sysvol\Program Files\Ethereal\libgdk_pixbuf-2.0-0.dll' size=0.11 MB file='libgdk_pixbuf-2.0-0.dll'>
    <filesystem/entry path='\sysvol\Program Files\Ethereal\libgmodule-2.0-0.dll' size=26.6 KB file='libgmodule-2.0-0.dll'>
    <filesystem/entry path='\sysvol\Program Files\Ethereal\libgobject-2.0-0.dll' size=0.25 MB file='libgobject-2.0-0.dll'>
    ....and many more....


Limiting
~~~~~~~~

The example above yields quite a lot records. Limiting the number of records can be done through
the ``--count`` and ``--skip`` options:

.. code-block:: console

    $ target-query host.img -f walkfs | rdump -s "r.path.suffix=='.dll'" -F path,file,size -E "file=path.name" --skip=1 --count=3

    <filesystem/entry path='\sysvol\My Documents\COMMANDS\cygwinb19.dll' size=0.38 MB file='cygwinb19.dll'>
    <filesystem/entry path='\sysvol\My Documents\ENUMERATION\NT\Cerberus\dnsscan.dll' size=40.0 KB file='dnsscan.dll'>
    <filesystem/entry path='\sysvol\My Documents\ENUMERATION\NT\Cerberus\fingerscan.dll' size=40.0 KB file='fingerscan.dll'>

Formatting
~~~~~~~~~~

A Python-style formatting rule can be specified using the ``-f`` option. The following example applies the format
``{file} {size}`` to the records:

.. code-block:: console

    $ target-query host.img -f walkfs | rdump -s "r.path.suffix=='.dll'" -F path,file,size -E "file=path.name" --skip=1 --count=3 -f "Filename: {file} Size: {size}"
    
    Filename: cygwinb19.dll Size: 0.38 MB
    Filename: dnsscan.dll Size: 40.0 KB
    Filename: fingerscan.dll Size: 40.0 KB

Instead of having to design your own format you can also choose one of these

* JSON (``-j`` or ``--mode=json``)
* CSV (``-C`` or ``--mode=csv``)
* Line (``-L`` or ``--mode=line``)

It is also possible let an adapter take care of the formatting. For instance, if you wish to have your
records in an archive format with a year-month-day folder structure, you can employ the ``-w`` option and
choose the archive adapter: ``archive://outputdir``. For complete list of adapters use ``-a``.

.. note::

    For a complete overview of all options see :doc:`here <tools/rdump>`.


