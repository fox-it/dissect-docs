target-shell
============

``target-shell`` gives you the ability to access a target using a virtual shell environment. Once a shell is opened
on a target, type ``help`` to list the available commands. To see the documentation of each command,
you can use ``help [COMMAND]``.

Opening a shell on a target is straight-forward. You can do so by specifying a path to a target as follows:

.. code-block:: console

    $ target-shell targets/EXAMPLE.vmx
    EXAMPLE /> help

    Documented commands (type help <topic>):
    ========================================
    cat    disks  filesystems  help     less  python    save
    cd     exit   find         hexdump  ls    readlink  stat
    clear  file   hash         info     pwd   registry  volumes

    EXAMPLE /> ls
    c:
    sysvol

Further interacting with the target can be done using the commands listed above. You can exit the shell by
running ``exit`` or pressing ``CTRL+D``.

Using ``target-shell`` on multiple targets opens a different prompt, this is called "Target Hub".
Within this hub you have the ability to choose the target you want to interact with.
Listing all targets in the hub can be done by using the ``list`` command.

To enter a specific target you can pass the index or hostname of that target to the ``enter`` command:

.. code-block:: console

    $ target-shell targets/*
    dissect> help

    Target Hub
    ==========
    List and enter targets by using 'list' and 'enter'.

    Documented commands (type help <topic>):
    ==============================================
    enter  exit  help  list  python

    dissect> list
    0: EXAMPLE
    1: EXAMPLE1
    3: EXAMPLE3
    4: EXAMPLE4

    dissect> enter 0
    EXAMPLE /> ls
    c:
    sysvol

When exitting a target specific shell, you return to the hub. Here you can enter another shell or re-enter the
previous target. Re-entering preserves your current path.

.. seealso::

    Please refer to :doc:`/usage/use-cases` for more examples of how to use ``target-shell``.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.shell
    :func: main
    :prog: target-shell
    :hook:

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.

The ``-p``, ``--python`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-p``, ``--python`` argument opens an interactive (I)Python shell on one or more targets. This gives you the
ability to programmatically interact with the one or more targets. Within this Python shell the first target is
loaded in the ``t`` variable, all other targets (including the first) are loaded in the ``targets`` variable.

.. code-block:: console

    $ target-shell -p targets/EXAMPLE.vmx
    Python 3.X.X
    Type 'copyright', 'credits' or 'license' for more information
    IPython X.X.X -- An enhanced Interactive Python. Type '?' for help.

    Loaded targets in 'targets' variable. First target is in 't'.

    In [1]: t, targets
    Out[1]: (<Target EXAMPLE.tar>, [<Target EXAMPLE.tar>])

    In [2]: t.hostname, targets[0].hostname
    Out[2]: ('EXAMPLE', 'EXAMPLE')

The ``-r``, ``--registry`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To directly examine the registry of a Windows target, the shell can be opened in registry mode with the
``-r``, ``--registry`` argument.

This registry shell lets you explore the registry as if it was a filesystem. Navigate through the keys with the ``cd``
command and show the value of a key with the ``cat`` command. Note, however, that to go back up the directory tree,
the ``up`` command should be used instead of using ``cd ..``. This is because ``..`` is a valid name for a registry
key or value.

.. code-block:: console

    $ target-shell targets/EXAMPLE.E01 -r
    EXAMPLE/registry > ls
    HKEY_LOCAL_MACHINE
    HKEY_USERS
    EXAMPLE/registry > cd HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NetFramework
    EXAMPLE/registry HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NetFramework> cat Enable64Bit
    value-shows-here
