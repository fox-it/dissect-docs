Disk encryption (FVE)
=====================

Dissect has support for transparent disk encryption. This means that, for supported disk encryption implementations,
all Dissect tools will be able to work transparently on the source data, without having to wait on a "decrypted copy"
of the source data.

For more information about supported full disk encryption implementations and API usage see 
the :ref:`projects/dissect.fve` project.

Keychains
---------

Because Dissect is designed to work on multiple :ref:`targets <overview/index:targets>`, we need a way to specify
one or more encryption keys for one or more targets. Dissect uses the concept of a keychain CSV file for this.

A valid keychain CSV file contains four columns, namely ``provider``, ``key_type``, ``identifier`` and ``value``.

.. csv-table::
    :header: "Column", "Description"

    "``provider``", "Optional, can be left blank. The encryption provider ID. E.g. ``bitlocker``."
    "``key_type``", "Required. The key type for this entry. One of ``passphrase``, ``recovery_key`` or ``file``."
    "``identifier``", "Optional, can be left blank. The UUID of the volume or data that corresponds to this key."
    "``value``", "Required. The key value. E.g. a user passphrase, Bitlocker recovery key or path to BEK file."

If no ``provider`` or ``identifier`` value is specified, decryption will be attempted by brute forcing using the
provided keys. This can be extremely slow, depending on the implementation, so it's recommended to enter as much
information in this file as you know.

For example, we may receive a Bitlocker recovery key but don't know the UUID that it corresponds to. We can run
a Dissect tool with ``INFO`` logging (``-v``) to learn if decryption succeeded and what the corresponding UUID is.
With this new knowledge, we can update the keychain file so that future invocations are faster.

.. code-block:: text
    :caption: Example keychain CSV file

    bitlocker,passphrase,b6ad258a-2725-4a42-93c6-844478bf7a90,Password1234
    ,passphrase,,AnotherTestPassword

The argument ``-K``, ``--keychain-file`` can be used with most Dissect tools to specify a keychain CSV
file. Alternatively, if you're only dealing with a single target or just want to quickly inspect something,
the ``-Kv``, ``--keychain-value`` argument can be used to easily specify a key passphrase, recovery key or a
key file on the command line without having to create a keychain CSV file.
