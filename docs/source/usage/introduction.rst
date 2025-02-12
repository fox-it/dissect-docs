Introduction
============

After installing Dissect by following the :ref:`installation steps <install/index>`, the Dissect
tools should be available to you.

To verify if the tooling is available, start by typing ``target-`` in your command line interface and press your
TAB key. It should look something like this:

.. code-block:: console

    $ target-<TAB>
    target-fs                target-query             target-shell
    target-dd                target-mount             target-reg

If you don't see this output, verify that your ``PATH`` is setup correctly to play nicely with your Python environment,
or that your Docker setup is functioning correctly.

All of these tools work on what we call :ref:`usage/introduction:targets`.

.. csv-table::
    :header: "Tool", "Description"

    ":doc:`/tools/acquire`", "Forensic artefact collection tool."
    ":doc:`/tools/target-query`", "Export artefacts (plugin outputs) from targets to stdout or a record file."
    ":doc:`/tools/target-shell`", "Interact with targets using a virtual shell."
    ":doc:`/tools/target-fs`", "Interact with a single target's filesystem via the command line."
    ":doc:`/tools/target-reg`", "Interact with the registry of a Windows based target."
    ":doc:`/tools/target-dump`", "Export artefacts in bulk to record files."
    ":doc:`/tools/target-dd`", "Export raw bytes from a target to stdout or a file."
    ":doc:`/tools/target-mount`", "Mount a target using FUSE."
    ":doc:`/tools/rdump`", "Dump, transform, and manipulate :ref:`records <overview/index:records>` from stdin or a file."

You can follow the tool link(s) to get a basic understanding of what these tools can do and how they operate.

Targets
-------

All the Dissect tools work on "targets". A target can best be described as "any data from a system that can be
used to describe a state of that system". This can range from a collection of separate files to a full disk image.

Examples of targets include but are not limited to:

* Physical hard disks: ``\\.\PHYSICALDRIVE#`` or ``/dev/sdX``
* Disk images: ``E01`` (Expert Witness Format) or ``RAW`` (dd)
* Virtual machine descriptors: ``vmx``, ``vmcx``, ``vbox``
* Virtual hard disks: ``vmdk`` or ``qcow2``
* Directory structure resembling the Windows or Unix filesystem hierarchy
* Tar archive(s) resembling a Windows or Unix filesystem hierarchy

.. seealso::

    For more information about targets, see :ref:`overview/index:targets`.

Basic usage
-----------

If all the Dissect tools are available to you as expected, you can immediately start exploring targets! Grab your
favourite disk image or virtual machine, and start by executing some simple Dissect commands. If you don't have
any data to play around with, you can download some Windows virtual machines from Microsoft
`here <https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/>`_, or use the images provided in NIST's
`Hacking Case <https://cfreds-archive.nist.gov/Hacking_Case.html>`_. From this case we will be using the ``SCHARDT``
image for some of these examples. This is also one of the images used in :doc:`use-cases </usage/use-cases>`.

Retrieving basic information with target-query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The best way to get started with Dissect is by using :doc:`/tools/target-query`. We can use ``target-query`` to query
information and artefacts from targets. We can retrieve a list of all available functions with the
``target-query --list`` command, which we'll cover in more detail later.

The following functions are not currently shown in the list ``target-query --list`` output, however they do exist:

* ``hostname``
* ``domain``
* ``os``
* ``version``
* ``ips``
* ``users``

The first four functions can be used together in one :doc:`target-query </tools/target-query>` command as their
``output`` type is the same:

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f hostname,domain,os,version,ips -d ';'
    <Target /mnt/SCHARDT.001> N-1A9ODN6ZXK4LQ;None;windows;Microsoft Windows XP (NT 5.1) 2600 ;['192.168.1.111']

With the ``-f`` argument we specified a function that we wanted to query, in this case the hostname, version, OS,
version and IPs. We see the result printed on the command line. We used ``-d`` to set ``;`` as delimiter, so you
can distinguish between the different outputs. These functions execute in order, so by changing it around, you will
get a different result.

Let's look at something a little more interesting. The behaviour of the ``users`` function is different depending on
the type of operating system. In other words, ``users`` looks different for ``windows`` and ``unix`` type systems,
but we can execute it the same on any target.

With the ``SCHARDT.001`` image, we get the following output:

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f users
    <windows/user hostname='N-1A9ODN6ZXK4LQ' domain=None sid='S-1-5-18' name='systemprofile' home='%systemroot%\\system32\\config\\systemprofile'>
    <windows/user hostname='N-1A9ODN6ZXK4LQ' domain=None sid='S-1-5-19' name='LocalService' home='%SystemDrive%\\Documents and Settings\\LocalService'>
    <windows/user hostname='N-1A9ODN6ZXK4LQ' domain=None sid='S-1-5-20' name='NetworkService' home='%SystemDrive%\\Documents and Settings\\NetworkService'>
    <windows/user hostname='N-1A9ODN6ZXK4LQ' domain=None sid='S-1-5-21-2000478354-688789844-1708537768-1003' name='Mr. Evil' home='%SystemDrive%\\Documents and Settings\\Mr. Evil'>

This time we specified a function that returns :ref:`records <overview/index:records>`. If we just run this as-is,
we see the records in human-readable form on the command line. Later on we will show you how to use :doc:`/tools/rdump` to
work with these records in interesting ways.

Querying for more in-depth information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the previous commands, we figured out information about the system and its users from the ``SCHARDT.001`` image.
Now that we know it is a ``windows`` machine, we can use some operating system specific functions to get more information.
We can retrieve a list of all available functions with the ``target-query --list`` command:

.. code-block:: console

    $ target-query -l
    [...]
    windows:
      [...]
      regf:
        [...]
        recentfilecache:
          recentfilecache - Parse RecentFileCache.bcf. (output: records)
        regf:
          regf - Return all registry keys and values. (output: records)
        runkeys:
          runkeys - Iterate various run key locations. See source for all locations. (output: records)
        shellbags:
          shellbags - Return Windows Shellbags. (output: records)
        shimcache:
          shimcache - Return the shimcache. (output: records)
        usb:
          usb - Return information about attached USB devices. (output: records)
        userassist:
          userassist - Return the UserAssist information for each user. (output: records)
    [...]

Note that the code block does not show the whole output, places that have been truncated are indicated with ``[...]``.

The list of functions will grow by contributions of the Dissect team and the community.
If you have an idea for a new plugin/function feel free to :doc:`contribute </contributing/developing>`.

Let's suppose we want to get more information about one of these functions, for example ``runkeys``. We can do so by supplying the ``--help`` option to said function.
This gives you a short description of the function, sources about the type of artefacts, and the kind of output you can expect.

.. code-block:: console

    $ target-query -f runkeys --help
    usage: target-query -f runkeys [-h]

    `runkeys` (output: records)

        Iterate various run key locations. See source for all locations.

        Run keys (Run and RunOnce) are registry keys that make a program run when a user logs on. a Run key runs every
        time the user logs on and the RunOnce key makes the program run once and deletes the key after. Often leveraged
        as a persistence mechanism.

        Sources:
            - https://docs.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys

        Yields RunKeyRecords with fields:
            hostname (string): The target hostname.
            domain (string): The target domain.
            ts (datetime): The registry key last modified timestamp.
            name (string): The run key name.
            path (string): The run key path.
            key (string): The source key for this run key.

    optional arguments:
      -h, --help  show this help message and exit

Now that we know what the function does, lets use it to get more information from the image.

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f runkeys
    <windows/registry/run hostname='N-1A9ODN6ZXK4LQ' domain=None ts=2004-08-19 23:04:32.009333+00:00 name='MSMSGS' path='"C:/Program Files/Messenger/msmsgs.exe" /background' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' regf_hive_path='sysvol/Documents and Settings/Mr. Evil/ntuser.dat' regf_key_path='$$$PROTO.HIV\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' username='Mr. Evil' user_id='S-1-5-21-2000478354-688789844-1708537768-1003' user_home='%SystemDrive%\\Documents and Settings\\Mr. Evil'>

So, the ``runkeys`` function shows that the ``Mr. Evil`` user account has one ``Run`` entry.
Additionally, Dissect adds additional ``user`` information for ``windows`` and ``unix`` hosts.
For ``windows``, this additional information includes:

* ``username``: The name of the user in question.
* ``user_id``: The SID or Security Identifier of that user.
* ``user_home``: The user its home directory.

And for specific Windows registry related functions, it also adds the following information:

* ``regf_hive_path``: The path of the registry hive.
* ``regf_key_path``: The registry key that was used inside the hive.

Using rdump to interact with the output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`/tools/rdump` is a tool you can use to interact and manipulate :ref:`records <overview/index:records>` with.
For this example, lets use rdump to manipulate the ``user`` records to only see the names with ``-F``:

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f users | rdump -F 'name'
    <windows/user name='systemprofile'>
    <windows/user name='LocalService'>
    <windows/user name='NetworkService'>
    <windows/user name='Mr. Evil'>

As you can see, we can use ``rdump`` to transform the output we get from the output of ``target-query``.
A more intricate example is to filter the output to only show the record where ``name='Mr. Evil'``:

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f users | rdump -s '"Mr. Evil" not in r.name' -X 'domain'
    <windows/user hostname='N-1A9ODN6ZXK4LQ' sid='S-1-5-21-2000478354-688789844-1708537768-1003' name='Mr. Evil' home='%SystemDrive%\\Documents and Settings\\Mr. Evil'>

We use the ``-s`` flag as a selector to select only those records that match the expression ``'"Mr. Evil" not in r.name'``.
In that example ``r`` refers to the current record.
The ``-X`` removes a field from the output, as ``domain`` is empty in this image, we use it to remove that field from the output.

Some other quick examples on what you can do with ``rdump``:

.. code-block:: console

    ## Write to a Splunk TCP ingestor
    $ target-query /mnt/SCHARDT.001 -f evtx | rdump -w splunk://127.0.0.1:1337
    ## Write to a file so we can do some processing with rdump later
    $ target-query /mnt/SCHARDT.001 -f shimcache > /tmp/shimcache.rec
    $ rdump /tmp/shimcache.rec

Neat, right? By default, records generated by ``target-query`` will be serialized into a binary format when piped
to a different command or file so that they can be deserialized and consumed by another command. We can enforce
the human-readable output by passing the ``-s``, ``--strings`` argument to ``target-query``. This allows for some
easy timelining as well:

.. code-block:: console

    $ target-query /mnt/SCHARDT.001 -f usnjrnl -s | sort > usnjrnl.txt

.. seealso::

    See :doc:`/tools/rdump` and :doc:`/usage/use-cases` for more documentation and examples on ``rdump``.

Browsing the target with target-shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you just want to have a quick browse around an image, or access some of the Python API of Dissect.
This is what :doc:`/tools/target-shell` enables. If we execute this on our target, we are dropped into a
virtual shell. Everything you see in this shell is completely virtual and parsed within Dissect:

.. code-block:: console

    $ target-shell /mnt/SCHARDT.001
    N-1A9ODN6ZXK4LQ /> info
    OS Plugin : WindowsPlugin

    Disks     :
    - <SplitContainer size=4871268352 vs=<DissectVolumeSystem serial=3965578333>>

    Volumes   :
    - <Volume name='part_00007e00' size=4869333504 fs=<NtfsFilesystem>>

    Hostname  : N-1A9ODN6ZXK4LQ
    OS        : Microsoft Windows XP (NT 5.1) 2600
    Domain    : None
    IPs       : ['192.168.1.111']

    N-1A9ODN6ZXK4LQ /> cd sysvol
    N-1A9ODN6ZXK4LQ /sysvol> cat boot.ini
    [boot loader]
    timeout=30
    default=multi(0)disk(0)rdisk(0)partition(1)\WINDOWS
    [operating systems]
    multi(0)disk(0)rdisk(0)partition(1)\WINDOWS="Microsoft Windows XP Professional" /fastdetect
    N-1A9ODN6ZXK4LQ /sysvol> cd Documents and Settings
    N-1A9ODN6ZXK4LQ /sysvol/Documents and Settings> ls
    All Users
    Default User
    LocalService
    Mr. Evil
    NetworkService

For more information on this virtual shell, run the ``help`` command within the shell or read the
:doc:`/tools/target-shell` documentation.

The ``-p``, ``--python`` argument drops you into a Python (or IPython if it is installed) REPL with the target(s)
loaded into the ``t`` and ``targets`` variable:

.. code-block:: console

    $ target-shell /mnt/SCHARDT.001 -p
    Python 3.10.5 (main, Jun  9 2022, 00:00:00) [GCC 12.1.1 20220507 (Red Hat 12.1.1-1)]
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.


    Loaded targets in 'targets' variable. First target is in 't'.

    In [1]: t.hostname
    Out[1]: 'N-1A9ODN6ZXK4LQ'

    In [2]: for path in t.fs.path("sysvol/Documents and Settings").iterdir():
    ...:     print(repr(path))
    ...:
    TargetPath('sysvol/Documents and Settings/All Users')
    TargetPath('sysvol/Documents and Settings/Default User')
    TargetPath('sysvol/Documents and Settings/LocalService')
    TargetPath('sysvol/Documents and Settings/Mr. Evil')
    TargetPath('sysvol/Documents and Settings/NetworkService')

Here you can play around with the full Dissect API.

.. seealso::

    To read more about what you can do here, navigate to :doc:`/advanced/api`.

Next steps
~~~~~~~~~~

Now you have a basic understanding on how to work with ``target-query`` and know how to execute different plugins on
a target. Furthermore, you know how to manipulate the output of ``target-query`` using ``rdump``.

Most of these tools can used be in combination with each other or other CLI tools. Please refer to the
:doc:`/usage/use-cases` page to see more in-depth examples on how to use these tools. If you just want to know more
about the different ``target-*`` tools, you can find it on the :doc:`/tools/index` page.
