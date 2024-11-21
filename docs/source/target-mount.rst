target-mount
------------

The target-mount tool allows you to **explore a forensic image** by mounting it as
a filesystem. To accomplish this, target-mount uses the ``FUSE`` library.

.. code-block:: console
    
    $ target-mount host.img /mnt/mountpoint
    
After the target has been mounted, you can explore the contents of the target using
regular file managers.

.. note::

    For a complete overview of all options see :doc:`here <tools/target-mount>`.
