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


Profiles
~~~~~~~~

By default, Acquire runs the full profile, meaning it will collect as much as it can.
You can select specific artefacts you are interested in or you can select a profile.

    
.. note::

    For a complete overview of all options see :doc:`here <tools/acquire>`.
    
    
    
