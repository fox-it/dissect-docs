Preparation
===========

The Dissect tutorial is designed so you can follow all the steps on your own computer! It comes with a set of example data to explore and we
highly recommend that you follow the preparation steps below so that your setup matches the examples.

The preparation steps are as follows:

1. Install Dissect
2. Download example data
3. Prepare directory structure
4. Test if the preparation steps are succesful

.. note::
    Although Dissect will work on Windows, a Unix based system is assumed in the rest of this tutorial. You may need to
    adjust some of the examples accordingly.


Install Dissect
---------------

Installing Dissect is easy and is described in :ref:`/index:Getting Started'`. For this tutorial, you can choose to install
the Python packages directly or use a Dissect Docker image. If you choose to use Docker for this tutorial, you may need to
change the commands in the examples; that is out of the scope of this tutorial.

To verify the succesful installation of Dissect, start by typing ``target-`` in your command line interface and press the
``TAB`` key. Your console will show something like this (the actual number of tools and order of appearance may differ):

.. code-block:: console

    $ target-<TAB>
    target-fs                target-query             target-shell
    target-dd                target-mount             target-reg

If you don't see this output, verify that your ``PATH`` is setup correctly to point to the proper Python environment,
or that your Docker setup is functioning correctly.


Download example data
---------------------

As Dissect is a tool for forensic investigations and incident response on anything
disk related (FIXME RAAR WOORD), we need data sets to demonstrate the tooling.

We have prepared two data sets that we use in the tutorial. One data set that was used for the NIST
`Hacking Case <https://cfreds-archive.nist.gov/Hacking_Case.html>`_ and the other set was prepared by us.


NIST data set
~~~~~~~~~~~~~

This data set consists of a ``dd`` (https://en.wikipedia.org/wiki/Dd_%28Unix%29) image (in multiple parts) and an
EnCase image (in two parts) of a laptop of a certain suspect in a forensic hacking case mentioned above.

Use the links below to download this data set:

* ``SCHARDT.001`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.001>`_, 636 MB)
* ``SCHARDT.002`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.002>`_, 636 MB)
* ``SCHARDT.003`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.003>`_, 636 MB)
* ``SCHARDT.004`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.004>`_, 636 MB)
* ``SCHARDT.005`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.005>`_, 636 MB)
* ``SCHARDT.006`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.006>`_, 636 MB)
* ``SCHARDT.007`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.007>`_, 636 MB)
* ``SCHARDT.008`` (DD image, `mirror <https://files.dissect.tools/images/SCHARDT.008>`_, 199 MB)
* ``4Dell Latitude CPi.E01`` (EnCase image, `mirror <https://files.dissect.tools/images/4Dell+Latitude+CPi.E01>`_, 641 MB)
* ``4Dell Latitude CPi.E02`` (EnCase image, `mirror <https://files.dissect.tools/images/4Dell+Latitude+CPi.E02>`_, 400 MB)
* ``IE11-Win81-VMWare-disk1.vmdk`` (Full VMDK file, `mirror <https://files.dissect.tools/images/IE11-Win81-VMWare-disk1.vmdk>`_, 8.0 GB)
* ``MSEDGEWIN10_20220708124036.tar``  (``acquire`` container, `mirror <https://files.dissect.tools/images/MSEDGEWIN10_20220708124036.tar>`_, 469 MB)

Fox-IT data set
~~~~~~~~~~~~~~~~~

This data set was made by us and contains two items:

1. VMWare disk image (``.vmdk``) of a IE11 Windows VM
2. a ``tar`` file which is the output of the Dissect tool :doc:`/tools/acquire` run on the ``.vmdk`` file of an MSEdge Windows VM. (you don't need to know what ``acquire`` is to continue)

The VMs used in this set were obtained from `Microsoft Developer Virtual Machines <https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/>`_.

Use the links below to download this data set:

* ``IE11-Win81-VMWare-disk1.vmdk`` (Full VMDK file, `mirror <https://files.dissect.tools/images/IE11-Win81-VMWare-disk1.vmdk>`_)
* ``MSEDGEWIN10_20220708124036.tar``  (``acquire`` container, `mirror <https://files.dissect.tools/images/MSEDGEWIN10_20220708124036.tar>`_)


Prepare directory structure
----------------------------

When doing investigations, it is important to create a consistent and structured directory layout. Setting up this layout has two steps:
creating directories and creating symlinks.

For the purpose of this tutorial, we ask you to follow the instructions below as all the examples in this tutorial
assume this directory structure.

.. note::
    For real investigations, a more elaborate layout is recommended and is described here FIXME.


.. warning::
    In the example commands below, we assume that the home directory is ``/home/user/``. Change the commands where needed
    to reflect your actual directory paths.


Creating directories
~~~~~~~~~~~~~~~~~~~~

Creating different directories for different types of data keeps your working environment neat and tidy. Also, since disk images
are often spread out over multiple large files, it helps to make a distinction between a logical 'disk image' and the actual
files they are made up (as is the case of SCHARDT.00x data set mentioned above).

A minimal working directory can be made by creating the following directories:

.. list-table:: Investigation directory structure
    :header-rows: 1
    :widths: 10 10 80

    * - Directory
      - Meaning
      - Description
    * - d/
      - Data
      - Raw source data. Organised as:

        * ``d/YYYYMMDD/Source folder``

        Data in this folder is ideally made immutable using ``chattr +i`` to avoid accidental deletion or
        modification.
    * - t/
      - Targets
      - Symbolic links to target source data from the ``d/`` folder. See :ref:`usage/first-steps/index:Creating symlinks`
        for a more elaborate description. FIXME

In the above, replace 'Source folder' with nist and fox to store the datasets respectively.

Your directory structure should look something like this:

.. code-block:: console

    $ find . | sort
    .
    ./d
    ./d/20230101
    ./d/20230101/fox
    ./d/20230101/fox/IE11-Win81-VMWare-disk1.vmdk
    ./d/20230101/fox/MSEDGEWIN10_20220708124036.tar
    ./d/20230101/nist
    ./d/20230101/nist/4Dell+Latitude+CPi.E01
    ./d/20230101/nist/4Dell+Latitude+CPi.E02
    ./d/20230101/nist/SCHARDT.001
    ./d/20230101/nist/SCHARDT.002
    ./d/20230101/nist/SCHARDT.003
    ./d/20230101/nist/SCHARDT.004
    ./d/20230101/nist/SCHARDT.005
    ./d/20230101/nist/SCHARDT.006
    ./d/20230101/nist/SCHARDT.007
    ./d/20230101/nist/SCHARDT.008
    ./t

Creating symlinks
~~~~~~~~~~~~~~~~~

When creating the investigation directory structure, you should also create symlinks to your target source data.
Creating symlinks to your targets is useful so that you can arbitrarily group your targets, without having to copy or
move actual files around. For example, all your original source data can stay in timestamped upload directories.
Then you can symlink the target files by host type (workstation, server), Windows AD domain, Windows AD forest,
or a combination hereof! FIXME REWRITE

Since in this case the DD and the EnCase image consist of multiple files, it's useful to create a symlink to the first
file so that you effectively have one target for the entire image (don't worry, Dissect can handle this!).

Let's create symlinks for all images and store them in the directory called ``t``.

.. code-block:: console

    $ ln -s /home/user/d/YYYYMMDD/fox/SCHARDT.001 /home/user/t/SCHARDT.001

Do the same for the other 3 image files so that your ``t`` directory contains the following links:

* ``4Dell Latitude CPi.E01``
* ``IE11-Win81-VMWare-disk1.vmdk``
* ``MSEDGEWIN10.tar``
* ``SCHARDT.001``

Now that we have all our targets neatly organized, we can progress to the next step!

Setup test
----------

You can now initiate the following command to see if Dissect is working on the data set you downloaded:

.. code-block:: console

    $ target-info t/IE11-Win81-VMWare-disk1.vmdk
    <Target t/IE11-Win81-VMWare-disk1.vmdk>

    Disks
    - <VmdkContainer size=42949672960 vs=<DissectVolumeSystem serial=2421862942>>

    Volumes
    - <Volume name='part_00100000' size=42947575808 fs=<NtfsFilesystem>>

    Hostname      : IE11WIN8_1
    Domain        : None
    IPs           : 192.168.108.130
    OS family     : windows (WindowsPlugin)
    OS version    : Windows 8.1 Enterprise Evaluation (NT 6.3) 9600.18874
    Architecture  : amd64-win64
    Language(s)   : en_US
    Timezone      : America/Los_Angeles
    Install date  : 2018-01-03 06:29:28+00:00
    Last activity : 2018-01-03 12:21:10.563210+00:00

Conclusion
----------

In this step you have succesfully installed Dissect, downloaded all necessary sample data and organized the directory structure on your computer
to match the examples of the tutorial.

