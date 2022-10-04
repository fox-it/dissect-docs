target-mount
============

With ``target-mount`` you can mount the filesystem of a target to an arbitrary directory on your analysis machine,
similar to the ``mount`` command on Unix systems.

``target-mount`` has two required positional arguments:

* ``TARGET`` - Target to mount
* ``MOUNT`` - Directory to mount the target's filesystem on

The following example command can be used to mount a target to the directory ``mnt``:

.. code-block:: console

    $ target-mount targets/EXAMPLE.vmx ~/mnt/EXAMPLE
    ## In a different shell
    $ ls ~/mnt/EXAMPLE/
    disks   fs   volumes

When mounting a target using ``target-mount`` the process is kept in the foreground. This will occupy your current
terminal session. It is recommended to either open a second terminal, let this command run in the background by
appending ``&`` to the command or use a terminal multiplexer like ``tmux`` to start a second session. Using one
of these methods enables you to interact with the mount point.

In the example above we mounted a VMware virtual machine. When looking at the directory listing of the mount point,
you will notice the folders ``disks``, ``fs``, and ``volumes``.

* The ``disks`` folder exposes the raw disks found by ``target-mount`` within the container file (in this case, one or more VMDK files).
* The ``fs`` folder exposes the filesystem folder hierarchy divided in their respective root folder.
* The ``volumes`` folder exposes the raw volumes found by ``target-mount`` (in this case, Windows NTFS volumes).

.. seealso::

    Please refer to :doc:`/usage/use-cases` for more examples of how to use ``target-mount``.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.mount
    :func: main
    :prog: target-mount
    :hook:

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.
