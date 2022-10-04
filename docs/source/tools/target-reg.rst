target-reg
==========

``target-reg`` is a tool to easily query the registry of Windows targets and prints it in a tree.
A ``+``symbol indicates that it is a registry key (i.e. may have subkeys). A ``-`` symbol indicates a registry value.

.. code-block:: console

    $ target-reg targets/EXAMPLE.E01 -k "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft"
    + 'Microsoft' (last-modified-date-shows-here)
      + '.NETFramework' (last-modified-date-shows-here)
        - 'Enable64Bit' value-shows-here
    [...]

.. seealso::

    Please refer to :doc:`/usage/use-cases` for more examples of how to use ``target-reg``.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.reg
    :func: main
    :prog: target-reg
    :hook:

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.

The ``-k``, ``--key`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next to the targets to query, the ``-k [KEY]`` key argument is a required argument. This is used to specify the key that
should be queried for. Be sure to put the key within quotation.

The ``-kv``, ``--value`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-kv``, ``--value`` argument can be used to specify the value that the queried key should contain. This comes in
when for example searching for legitimate keys with a known malicious value.

The ``-d``, ``--depth`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-d``, ``--depth`` argument is used to specify the depth level of the queried key. When example querying the key
``HKEY_LOCAL_MACHINE`` with a depth level of 1, the result will show all the hives that are present within
(SAM, SECURITY, SOFTWARE, etc.). However, all these hives contain keys within, which means they are at depth
level 2 seen from ``HKEY_LOCAL_MACHINE``. As you can guess, this next level can be made visible using ``-d 2``.

.. code-block:: console
    :caption: Example usage of the ``-d``, ``--depth`` argument

    $ target-reg targets/EXAMPLE.E01 -k "HKEY_LOCAL_MACHINE" -d 1
    + 'HKEY_LOCAL_MACHINE' (None)
      + 'SAM' (last-modified-date-shows-here)
      + 'SECURITY' (last-modified-date-shows-here)
    ...
    $ target-reg targets/EXAMPLE.E01 -k "HKEY_LOCAL_MACHINE" -d 2
    + 'HKEY_LOCAL_MACHINE' (None)
      + 'SAM' (last-modified-date-shows-here)
        + 'SAM' (last-modified-date-shows-here)
          - 'C' value-shows-here
          - 'ServerDomainUpdates' value-shows-here
     + 'SECURITY' (last-modified-date-shows-here)
        + 'Cache' (last-modified-date-shows-here)
          - 'NL$1' value-shows-here
    ...
