Next steps as an Incident Handler
=================================

As an Incident Handler, you wish to perform quick triage and find patient-zero as soon as possible. Dissect has
some great features to help you with this! The following steps will guide you through quickly obtaining essential
information from potentially affected machines and how to analyse the critical information afterwards.

Creating a forensic container
-----------------------------

In case of a larger incident, you'll probably have multiple suspect machines or important crown jewels that you want to
investigate as soon as possible. These can be large servers or virtual disks, where taking a full forensic image
is a slow process. On top of that, most of the copied information might not be relevant for the incident at hand.
:doc:`/tools/acquire` has especially been developed to help in this situation. It is capable of rapidly collecting the
most essential information from a (live) system into a small sized container (0.5-3.0 GB).

Usually, you'll find yourself in a situation where you want to make an image of a live system. But for this example,
let's say you wish to have a lightweight forensic container of ``IE11-Win81-VMWare-disk1.vmdk``, instead of the full
VMDK file. Using Acquire with the ``minimal`` profile results in obtaining the basic relevant artefacts in a small
sized container.

Let's run ``acquire`` on the ``.vmdk`` file and compare the file sizes afterwards.

.. code-block:: console

    $ acquire targets/IE11-Win81-VMWare-disk1.vmdk --profile minimal
    [...]
    $ du targets/{*.vmdk,*.tar} -sh
    8.0G    ./IE11-Win81-VMWare-disk1.vmdk
    469M    ./MSEDGEWIN10.tar

We end up with a 0.5 GB ``acquire`` container, which is 17 times smaller than the original 8 GB ``.vmdk``!

.. seealso::

    Refer to :doc:`/tools/acquire` for a more in-depth explanation of what ``acquire`` can do.


If you want to obtain artefacts on a larger scale, you can do so using the examples described in :ref:`tools/acquire:deployment`. 
It allows you to pack Acquire into a standalone executeable and deploy it in a network!

Creating an MFT timeline
------------------------

In case of a NTFS file system, creating an MFT timeline is a great way to get a quick initial impression of what
happened on a system. To create such a timeline, we can use the special ``mft_timeline`` function. It parses the MFT
file and returns a human readable output. Since the MFT is an important artefact in the context of digital forensics,
the ``minimal`` Acquire profile collects this file. To show this, we use the ``MSEDGEWIN10.tar`` as a target to produce
the MFT timeline with the following command:

.. code-block:: console

    $ target-query targets/MSEDGEWIN10.tar -f mft_timeline | sort > MSEDGEWIN10_timeline.txt
    $ cat MSEDGEWIN10_timeline.txt
    [...]
    2020-08-10 15:53:20+00:00 SM 105369 c:\Windows\System32\CatRoot\{F7 50E6C3-38EE-11D1-85E5-00C04FC295EE}\oem3.cat - InUse:True Resident:False Owner:S-1-5-18 Size:10333 VolumeUUID:3fa6fe91-916a-4c89-ab18-cd58de1c8fab
    2020-08-10 15:53:22+00:00 SB 105154 c:\Program Files\Common Files\VMware\Drivers\efifw\Win8\efifwver.dll - InUse:True Resident:False Owner:S-1-5-18 Size:2048 VolumeUUID:3fa6fe91-916a-4c89-ab18-cd58de1c8fab
    2020-08-10 15:53:22+00:00 SM 105154 c:\Program Files\Common Files\VMware\Drivers\efifw\Win8\efifwver.dll - InUse:True Resident:False Owner:S-1-5-18 Size:2048 VolumeUUID:3fa6fe91-916a-4c89-ab18-cd58de1c8fab
    2021-01-22 10:01:00+00:00 F1C 684 c:\Users\Default\Downloads\random_01.dll - InUse:True Resident:False Owner:S-1-5-32-544 Size:3443712 VolumeUUID:3fa6fe91-916a-4c89-ab18-cd58de1c8fab
    [...]

After ``sort`` is complete you can open the MFT timeline in your favorite text editor / pager like ``vim`` or ``less``
and use common text manipulation tools such as ``grep``, ``rg``, or ``awk`` to start your triage!

This example is not limited to the ``mft_timeline`` function. For example, for the Windows event logs we can achieve the same thing with a similar command:

.. code-block:: console

    $ target-query targets/MSEDGEWIN10.tar -f evtx -s | sort > MSEDGEWIN10_evtx.txt

Note that we have to add the ``-s`` (or ``--string``) argument now to get human readable output, because the ``evt`` and ``evtx`` functions
return records, whereas the ``mft_timeline`` directly returned lines of text.

Look for signs of persistence
-----------------------------

Once attackers gain access to a system, it is quite likely that they want to use some sort of persistence. 
Since it's crucial for a digital forensic investigation to find possible used persistence techniques, we would
like to check the locations signs of persistence can be found for each target. Some of the functions we can use include:

* ``runkeys``
* ``services``
* ``tasks``
* ``clsid``
* ``startupinfo``

Let's use them by running the following command:

.. code-block:: console

    $ target-query targets/ -f runkeys,services,tasks,clsid,startupinfo

For analysis of the results, you can use your favourite search platform or perform a similar search as explained in the
investigation steps for a security analyst like :ref:`usage/first-steps/security-analyst:finding hijacked clsids`.

Write ``target-query`` functions output to a file
-------------------------------------------------

:doc:`/tools/target-query` will quickly become your best friend during an investigation. 
From the :doc:`/usage/introduction` page, you've seen how you can easily query information and artefacts
from your targets by using the functions that are available to you. There are a couple of functions that return
information and artefacts that you would almost always want to take a look at during an investigation, including but not limited to:

* ``evtx``
* ``evt``
* ``mft``
* ``usnjrnl``
* ``prefetch``
* ``services``
* ``tasks``
* ``cronjobs``
* ``bashhistory``
* ``btmp``, ``wtmp``

Since time is an Incident Handler's worst enemy, you probably don't want to run each of these function separately for
each target. Therefore, let's create a small bash script that loops over these functions and writes the output to
separate output files:

.. code-block:: bash

    #!/bin/bash
    functions=("evt" "evtx") # add additional plugins to be executed plugins as you see fit!
    find targets/ -type l -print0 |
        while IFS= read -r -d '' t; do
            target=$(basename "$t")
            echo "[+] Running functions for target: $t"
            mkdir -p "host/$target"
            for f in ${functions[@]}; do
                    echo "[-] Running function $f"
                    target-query $t -f $f -q 2>> "host/$target/$f.log" > "host/$target/$f.rec"
            done
        done

Now, for each host in the ``host/`` folder, we have separate record files for each function. Note that some functions
are OS based, which make them incompatible with another OS. However, ``target-query`` will just skip a target when the
function is not compatible (which can be seen in the log files). So there is no need to change the essential function
list for each target.

To further speed up this process, you could use ``xargs`` to run multiple instances of ``target-query`` at the same time.

Load records into a search platform
-----------------------------------

One of the things you probably wish to do with the obtained records, is importing them to your search platform of
choice. We will discuss how to do this for two of the common ones here, namely Splunk and Elastic Search. Using
:doc:`/tools/rdump` makes this really easy, since it contains adapters for both of these. These adapters can be
invoked when using ``rdump`` in combination with the ``-w`` parameter.

.. note::

    ``rdump`` can produce Elastic and Splunk compatible output out of the box. Setting up these environments is left as
    an exercise to the reader.

Now, let's assume that we are running the search platforms on our local machine (port 1337 and 1338 for Splunk and Elastic,
respectively). The following small bash script will import all record files in the ``host/`` directory to the platforms:

.. code-block:: bash

  #!/bin/bash
  find host/ -type f -print0 |
      while IFS= read -r -d '' r; do
          echo "[+] Importing $r into search platforms"
          rdump "$r" -w splunk://localhost:1337 2>> "${r%.log}"
          rdump "$r" -w elastic://localhost:1338 2>> "${r%.log}"
      done
