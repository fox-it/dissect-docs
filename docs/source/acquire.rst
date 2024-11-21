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
Output
~~~~~~~~
By default, an acquire operation will result in 3 files:

    - a log file (the contents of this file will also appear on the screen)
    - a report file in JSON
    - a tar file that contains the requested artefacts

You can feed the resulting tar to tools like :doc:`target-query <tools/target-query>`, as shown below:

.. code-block:: console

    $ target-query N-1A9ODN6ZXK4LQ_20240502133639.tar -f ips
    <Target N-1A9ODN6ZXK4LQ_20240502133639.tar> ['192.168.1.111']


Profiles
~~~~~~~~


By design, Acquire runs with the ``default`` profile,
providing a curated selection of artifacts that aims to fulfill the
requirements of most scenarios efficiently.
This prefabricated suite encompasses a balanced assortment
designed to deliver comprehensive results without extensive processing time.
Alternatively, users have the flexibility to tailor their collection process by choosing
individual artifacts of interest or by opting for a different predefined
profile to suit their specific needs.

Selecting a single artefact:

.. code-block:: console

    $ acquire --evtx 

Selecting an acquisition profile:

.. code-block:: console

    $ acquire --profile full 

You can select a profile with the ``--profile`` option.
There are 4 basic profiles ``full``, ``default``, ``minimal`` and ``none``.
    
.. note::

    For a complete overview of the basic profiles see :doc:`here <tools/acquire>`.
