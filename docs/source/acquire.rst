acquire
-------

Acquire can **collect forensic artefacts** from a live system or an image. Resulting images
can be fed to other Dissect tools like target-query.

To run **acquire** on a live system:

.. code-block:: console
    
    $ acquire

.. note::

    To be able to access the full system to collect all its artefacts one must
    run acquire with administrator privileges.

By default, an acquire operation will result in 3 files:

    - a log file (the contents of this file will also appear on the screen)
    - a report file in JSON
    - a tar file that contains the requested artefacts

You can feed the resulting tar to tools like :doc:`target-query <tools/target-query>`.
again.

.. code-block:: console

    $ target-query N-1A9ODN6ZXK4LQ_20240502133639.tar -f ips
    <Target N-1A9ODN6ZXK4LQ_20240502133639.tar> ['192.168.1.111']


Profiles
~~~~~~~~

By default, Acquire runs the ``full`` profile, meaning it will collect as much as it can.
You can select specific artefacts you are interested in or you can select a profile.

Selecting a single artefact:
.. code-block:: console

    $ acquire --evtx 

Selecting a acquisition profile:
.. code-block:: console

    $ acquire --profile full 

You can select a profiles with the ``--profile`` option.
There are 4 basic profiles ``full`` (default), ``default``, ``minimal`` and ``none``.
    
.. note::

    For a complete overview of all options see :doc:`here <tools/acquire>`.
    
    
    
