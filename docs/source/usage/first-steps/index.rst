First steps
===========

.. toctree::
    :hidden:

    /usage/first-steps/incident-handler
    /usage/first-steps/security-analyst

After reading the :doc:`/usage/introduction` page, you are ready to tackle your first digital forensics and/or incident
response case with Dissect. This page will guide you through your first steps, taking you by the hand through the
process.

As case material, we're using the images provided by NIST for the
`Hacking Case <https://cfreds-archive.nist.gov/Hacking_Case.html>`_. This case consists of a DD image (in multiple
parts) and an EnCase image (in two parts) of a laptop of a certain suspect. Next to these two images, we've added
a ``.vmdk`` file from an IE11 Windows VM and an :doc:`/tools/acquire` container from the ``.vmdk`` file of
an MSEdge Windows VM. These VM images were obtained from
`Microsoft Developer Virtual Machines <https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/>`_.

Our investigation material consists of:

* `SCHARDT.001 <https://files.dissect.tools/images/SCHARDT.001>`_ (raw image, 636 MB)
* `SCHARDT.002 <https://files.dissect.tools/images/SCHARDT.002>`_ (raw image, 636 MB)
* `SCHARDT.004 <https://files.dissect.tools/images/SCHARDT.004>`_ (raw image, 636 MB)
* `SCHARDT.005 <https://files.dissect.tools/images/SCHARDT.005>`_ (raw image, 636 MB)
* `SCHARDT.006 <https://files.dissect.tools/images/SCHARDT.006>`_ (raw image, 636 MB)
* `SCHARDT.007 <https://files.dissect.tools/images/SCHARDT.007>`_ (raw image, 636 MB)
* `SCHARDT.008 <https://files.dissect.tools/images/SCHARDT.008>`_ (raw image, 199 MB)
* `4Dell Latitude CPi.E01 <https://files.dissect.tools/images/4Dell+Latitude+CPi.E01>`_ (EnCase image, 641 MB)
* `4Dell Latitude CPi.E02 <https://files.dissect.tools/images/4Dell+Latitude+CPi.E02>`_ (EnCase image, 400 MB)
* `IE11-Win81-VMWare-disk1.vmdk <https://files.dissect.tools/images/IE11-Win81-VMWare-disk1.vmdk>`_ (Full VMDK file, 8.0 GB)
* `MSEDGEWIN10_20220708124036.tar <https://files.dissect.tools/images/MSEDGEWIN10_20220708124036.tar>`_ (``acquire`` container, 469 MB)

While Dissect will work fine under Windows, a Unix based system is assumed when following along with these first steps.

Investigation directory structure
---------------------------------

Before starting your investigation with Dissect, it is advised to create a consistent and structured investigation
directory. The following table shows an example of what we at Fox-IT use:

.. list-table:: Investigation directory structure
    :header-rows: 1

    * - Directory
      - Abbreviation
      - Description
    * - data/
      - d/
      - Often abbreviated to ``d/``. Raw source data. Organised as:

        * ``d/YYYYMMDD/Source folder``

        Data in these folder is ideally made immutable using ``chattr +i`` to avoid accidentally deletion or
        modification.
    * - targets/
      - t/
      - Often abbreviated to ``t/``. Symbolic links to target source data from the ``d/`` folder. See :ref:`usage/first-steps/index:Creating symlinks`
        for a more elaborate description.
    * - host/
      - h/
      - Often abbreviated to ``h/``. Exported host data per hostname, such as ``mft_timeline`` results, ``evtx`` records, interesting binaries, etc.

        Organised per hostname as:

        * ``h/HOSTNAME/mft_timeline.txt``
        * ``h/HOSTNAME/evtx.rec``
        * ``h/HOSTNAME/beacon.bin``
    * - export/
      - e/
      - Often abbreviated to ``e/``. Actionable export data you either want to share with the client or use in some external tool, such as:

        * Overview of compromised machines
        * CMDBs
        * Files / data you want to share with client
        * Files / data you want to use in final report or presentation
        * Interesting binaries
    * - mount/
      - m/
      - Often abbreviated to ``m/``. Mounted images from the d/ directory, organised per hostname.

        * ``m/HOSTNAME/<filesystem_structure>``
        * ``m/HOSTNAME/ewf/ewf1``

Creating symlinks
-----------------

When creating the investigation directory structure, you should also create symlinks to your target source data.
Creating symlinks to your targets is useful so that you can arbitrarily group your targets, without having to copy or
move actual files around. For example, all your original source data can stay in timestamped upload directories.
Then you can symlink the target files by host type (workstation, server), Windows AD domain, Windows AD forest,
or a combination hereof!

Since in this case the DD and the EnCase image consist of multiple files, it's useful to create a symlink to the first
file such that you effectively have one target for the entire image (don't worry, Dissect can handle this!).
Normally we would symlink the ``.vmx`` file of the VM, but our sample case material doesn't, so we take the ``.vmdk`` file instead.

Let's create symlinks for all images and store them in a directory called ``targets/``.

.. code-block:: console

    $ ln -s /home/user/SCHARDT.001 /home/user/targets/SCHARDT.001

After all the symlinks have been created, the ``target/`` directory contains the following links:

* ``4Dell Latitude CPi.E01``
* ``IE11-Win81-VMWare-disk1.vmdk``
* ``MSEDGEWIN10.tar``
* ``SCHARDT.001``

Now that we have all our targets neatly organized, we can progress to the next step!

Creating a simple CMDB
----------------------

During most investigations, you want to keep track of the investigation material by creating your own simple CMDB. Dissect can do this for you!
As explained in :doc:`/tools/target-query`, you can create a CMDB using ``target-query``. Simply use the
``--cmdb`` argument, while using the basic OS functions. You can write this to a csv file to archive your CMDB.

.. code-block:: console

    $ target-query targets/ -f hostname,domain,OS,version,ips --cmdb -d ";" > export/CMDB.csv

The created csv file now contains the basic information about all the targets stored in the ``targets/`` directory. When
new targets are added to the directory, you can simply rerun the command to update your csv file.

Next steps
----------

You can click the cards below to navigate to your preferred next steps depending on your interest or role!

.. card:: Incident Handler
    :link: /usage/first-steps/incident-handler
    :link-type: doc

    Continue with basic analysis, typically useful for Incident Handlers.

.. card:: Security Analyst
    :link: /usage/first-steps/security-analyst
    :link-type: doc

    Continue with more advanced analysis tasks, typically useful for Security Analysts.
