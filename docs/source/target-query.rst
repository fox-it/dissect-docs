target-query
------------

The **target-query** tool is one of the most prominent tools of Dissect. It allows you to
**query a forensic image**
to extract useful information from it. The basic usage format is:

.. code-block:: console

    $ target-query <TARGET> -f <FUNCTION_NAME>

Here <TARGET> is the file you wish to query. In most cases this is a forensic image. 
<FUNCTION_NAME> is the name of the function you wish to apply.

Loading
~~~~~~~


By default, Dissect attempts to determine the file format automatically and selects the appropriate loader.
If the image is split into multiple files, just feed it the first. (For example with an EWF image, just target the 
.E01 file) 

If you wish to override auto-detection, use the ``-L`` option to explicitly specify the loader that
has to be used:

.. code-block:: console

    $ target-query host123.vdi -L vbox

.. note ::

    The full list of loaders is listed at the end of the output of the ``-l`` option.


In case there is no complete image available but just a couple of separate (log/evt/evtx) files, you can use
the LogLoader for example:

.. code-block:: console

    $ target-query data/*.evtx -L log -f evtx

It is also possible to load multiple separate disks, just string them together using the ``+`` character.

.. code-block:: console

    $ target-query disk1+disk2+disk3 -f osinfo
    
For encrypted disks like LUKS you can provide a key through the ``-K`` option to provide a keychain file
or ``-Kv`` to provide a passphrase.

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.

    
Querying
~~~~~~~~

To get a full list of all functions available in target-query use the ``-l`` option. If you provide a target image
the list will be filtered based on the compatibility with the target.

You can apply multiple functions if you want:

.. code-block:: console

    $ target-query host.img -f runkeys,users
    
.. note ::

    You can only combine functions that have the same output type.
    If you don't, only the records will be shown.
    
If you have a lot of functions you wish to apply, wildcards (and other glob-rules) can be used:

.. code-block:: console

    $ target-query host.img -f apps.browser.*.history
    
You can combine the ``-f`` option with the `dry-run` option (``-n``/``--dry-run``) to see what will be actually executed:

.. code-block:: console
    
    target-query host.img -n -q -f apps.browser.*.history
    
Excluding functions is possible with the ``-xf`` flag.

Plugins
~~~~~~~

Each function available in **target-query** is actually a plugin.
Creating your own plugins is also possible. With the ``--plugin-path`` flag you can point
Dissect to your own plugin folder:

.. code-block:: console
    
    target-query host.img -f myplugin --plugin-path=/myplugins


Output
~~~~~~

In most cases, your query will result in records. However there are in fact three output types
to consider:

* Records
* Lines
* Text

Types cannot be mixed. If you mix types, you only get the records.
Besides regular output, target-query may emit warnings, to suppress these use the ``-q`` option.

To limit the number of results, use the ``--limit`` option like this:

.. code-block:: console
    
    $ target-query host.img -f walkfs --limit 10

Besides the regular format, target-query can use ``-j`` option to output as JSON.
After you have generated some data you might want to process it further, you can use
:doc:`rdump <rdump>` (Record Dumper) for this.

.. note::

    For a complete overview of all options see :doc:`here <tools/target-query>`.
