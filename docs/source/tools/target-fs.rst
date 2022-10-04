target-fs
=========

With ``target-fs`` you can interact with the filesystem of a target, using a set of familiar Unix commands.

.. code-block:: console

    $ target-fs <path_to_target> <command> <path_for_command>

.. note::

    As with any shell command, you have to properly escape backlashes and spaces. Unless you use single or double quotes (``'``, ``"``).

Usage
-----

.. The argparse generation unfortunately doesn't play nicely with how we do arguments for target-fs
.. Write it all out for this one...

target-fs - CLI interface
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: default

    target-fs [-h] [-K KEYCHAIN_FILE] [-Kv KEYCHAIN_VALUE] [-v] [-q] TARGET {ls,cat,walk,cp} ...

target-fs positional arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``TARGET`` - Target to load (default: ``None``)
* ``{ls,cat,walk,cp}`` - Subcommand to execute

target-fs subcommands
~~~~~~~~~~~~~~~~~~~~~
* ``ls PATH`` - Show a directory listing
* ``cat PATH`` - Dump file contents
* ``walk PATH`` - Perform a walk
* ``cp PATH -o, --output OUTPUT`` - Copy multiple files to a directory specified by ``--output``

target-fs optional arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``-K`` ``KEYCHAIN_FILE``, ``--keychain-file`` ``KEYCHAIN_FILE`` - keychain file in CSV format (default: ``None``)
* ``-Kv`` ``KEYCHAIN_VALUE``, ``--keychain-value`` ``KEYCHAIN_VALUE`` - passphrase, recovery key or key file path value (default: ``None``)
* ``-v``, ``--verbose`` - increase output verbosity (default: 0)
* ``-q``, ``--quiet`` - do not output logging information

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.

The ``ls`` subcommand
^^^^^^^^^^^^^^^^^^^^^^

The ``ls`` command lets you list the directory contents of any path within the target.

.. code-block:: console

    $ target-fs targets/EXAMPLE.vmx ls "C:\Users"
    ## Or
    $ target-fs targets/EXAMPLE.vmx ls C:\\Users
    All Users
    Default
    Default User
    Public
    User
    desktop.ini

When interacting with a \*nix target you should supply a Unix like path instead.

The ``cat`` subcommand
^^^^^^^^^^^^^^^^^^^^^^

Using ``target-fs``'s ``cat`` subcommand it is possible to dump file contents from a target filesystem to stdout or
your local disk.

.. code-block:: console

    $ target-fs targets/EXAMPLE.vmx cat C:\\Windows\\NTDS\\NTDS.dit

If you want to save the file to your local disk, you can so by redirecting stdout to a filename of your choice.

The ``walk`` subcommand
^^^^^^^^^^^^^^^^^^^^^^^

Using the ``walk`` subcommand you are able to perform a walk of a specific target's directory. This will list every
file and folder recursively from the path specified to the ``walk`` subcommand.

.. code-block:: console

    $ target-fs targets/EXAMPLE.E01 walk C:\\Users\\EXAMPLE\\Desktop
    C:/Users/EXAMPLE/desktop/EXAMPLE.log
    C:/Users/EXAMPLE/desktop/EXAMPLE.report.json
    C:/Users/EXAMPLE/desktop/EXAMPLE.tar
    C:/Users/EXAMPLE/desktop/desktop.ini
    C:/Users/EXAMPLE/desktop/Windows Terminal.lnk
    C:/Users/EXAMPLE/desktop/winpmem.exe

The ``cp`` subcommand
^^^^^^^^^^^^^^^^^^^^^

Using the ``cp`` subcommand you have the ability to recursively copy folders or files from a specified path.
You can also supply the ``cp`` with an output directory, by using the ``-o <PATH>`` or ``--output <PATH>`` arguments.
When no output directory is configured, the current working directory will be used to save the files.

.. code-block:: console

    ## Copying the Config folder of a target to the current working directory
    $ target-fs targets/EXAMPLE.vmx cp C:\\Windows\System32\\Config
    C:\Windows\System32\Config\BBI -> /home/user/BBI
    C:\Windows\System32\Config\BBI.LOG1 -> /home/user/BBI.LOG1
    C:\Windows\System32\Config\BBI.LOG2 -> /home/user/BBI.LOG2
    [...]

    ## Copying the Config folder of a target to the current working directory
    $ target-fs targets/EXAMPLE.vmx cp C:\\Windows\System32\\Config -o reg/
    C:\Windows\System32\Config\BBI -> /home/user/reg/BBI
    C:\Windows\System32\Config\BBI.LOG1 -> /home/user/reg/BBI.LOG1
    C:\Windows\System32\Config\BBI.LOG2 -> /home/user/reg/BBI.LOG2
    [...]

    ## Copying a specific file in the Config folder of a target
    $ target-fs targets/EXAMPLE.vmx cp C:\\Windows\System32\\Config\\SECURITY -o reg/
    C:\Windows\System32\Config\SECURITY -> /home/users/reg/SECURITY
