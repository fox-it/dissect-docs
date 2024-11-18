target-shell
------------

The target-shell tool allows you to **explore a forensic image** as if you were navigating it through
a shell. 
Opening a target shell is as simple as:

.. code-block:: console
    
    $ target-shell host.img
    
After the target has been loaded, something like this will appear:

.. code-block:: console

    HOSTNAME />
    
This is the shell prompt, you can now list the contents of the current folder with ``ls``:

.. code-block:: console

    HOSTNAME /> ls
    c:
    sysvol
    
With ``cd`` you can change the directory, so with cd c:/windows/system32 you will
enter the system32 folder of the machine. Use ``exit`` to exit the shell.


.. note ::

    Although we are navigating a Windows machine here, the POSIX path notation
    is required.
    
Use ``cat`` to view the contents of text files (use ``zcat`` for compressed files and
``hexdump`` for binary files).

If you see an interesting file or directory you can save it to your local disk with:

.. code-block:: console

    /> save <FILENAME>

To search the file system utilize the ``find`` command like this:

.. code-block:: console

    /> find -name kernel*

Besides exploring the contents of the disk, you can use target-shell to
explore the registry as well (on Unixy systems you can explore the configuration
tree under /etc in a similar way).

.. code-block:: console

    N-1A9ODN6ZXK4LQ /> registry
    N-1A9ODN6ZXK4LQ/registry > ls
    HKEY_LOCAL_MACHINE
    HKEY_USERS


.. note::

    There are many more commands available, to see them all, simply enter ``help``.
    On top of that, every command has its own ``-h`` flag for a detailed description
    of all its available options.

For a complete overview of all options see :doc:`here <tools/target-shell>`.










