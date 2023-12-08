acquire
=======

``acquire`` is a tool to quickly gather forensic artifacts from disk images or a live system into a lightweight container.
This makes ``acquire`` an excellent tool to, among others, speed up the process of digital forensic triage.
``acquire`` uses ``dissect`` to gather forensic artifacts from the raw disk, if possible.

The most basic usage of ``acquire`` is as follows:

.. code-block:: console

    $ sudo acquire

The tool requires administrative access to read raw disk data instead of using the operating system for file access.
However, there are some options available to use the operating system as a fallback option. (e.g ``--fallback`` or ``--force-fallback``)


Filesystem information
----------------------

``acquire`` gathers artifacts based on modules. 
These modules are paths or globs on a filesystem which acquire attempts to gather.
Multiple modules can be executed at once, which have been collected together inside a profile.
These profiles (used with ``--profile``) are  ``full``, ``default``, ``minimal`` and ``none``.
Depending on the detected operating system, different artifacts are collected.

The following list shows the modules belonging to each ``profile``.

.. code-block:: text

    full profile:
      windows: NTFS, EventLogs, Registry, Tasks, PowerShell,
               Prefetch, Appcompat, PCA, Misc, ETL, Recents,
               RecycleBin, Drivers, Syscache, WBEM, AV, BITS,
               DHCP, DNS, ActiveDirectory, RemoteAccess,
               ActivitiesCache, History, NTDS, QuarantinedFiles,
               WindowsNotifications, SSH, IIS
      linux  : Etc, Boot, Home, SSH, Var, History, WebHosting
      bsd    : Etc, Boot, Home, SSH, Var, BSD
      esxi   : Bootbanks, ESXi, SSH, VMFS
      osx    : Etc, Home, Var, OSX, OSXApplicationsInfo, History,
               SSH

    default profile:
      windows: NTFS, EventLogs, Registry, Tasks, PowerShell,
               Prefetch, Appcompat, PCA, Misc, ETL, Recents,
               RecycleBin, Drivers, Syscache, WBEM, AV, BITS,
               DHCP, DNS, ActiveDirectory, RemoteAccess,
               ActivitiesCache
      linux  : Etc, Boot, Home, SSH, Var
      bsd    : Etc, Boot, Home, SSH, Var, BSD
      esxi   : Bootbanks, ESXi, SSH, VMFS
      osx    : Etc, Home, Var, OSX, OSXApplicationsInfo

    minimal profile:
      windows: NTFS, EventLogs, Registry, Tasks, PowerShell,
               Prefetch, Appcompat, PCA, Misc
      linux  : Etc, Boot, Home, SSH, Var
      bsd    : Etc, Boot, Home, SSH, Var, BSD
      esxi   : Bootbanks, ESXi, SSH
      osx    : Etc, Home, Var, OSX, OSXApplicationsInfo


Profile ``none`` is a special case where no module gets collected.
This profile, is used in combination with ``--dir``, ``--file`` or ``--glob`` to collect specific paths from a target.
These arguments do the following:

* ``--dir``: Collects a directory recursively.
* ``--file``: Collects one specific file.
* ``--glob``: Collects any file or directory that matches the specific glob pattern. (e.g ``/path*/test`` would collect for example ``/path1/test`` and ``/path_to_other_test_file/test``)

You can specify these arguments multiple times for every file, directory or glob you want to collect.

Volatile information
--------------------

Acquire has support for volatile information collection.
In other words, information that will be lost once a computer shuts off.
These are special modules that will only be executed at the end of all the other modules.

Acquire collects volatile windows information using this methods, which it stores in the ``$metadata$`` directory inside the acquire container.

* commands: Specific commands, either cmd or powershell.
* ctypes: Calling windows internals with python to store information.

For linux systems, acquire uses a volatile stream to interpret the ``proc`` and ``sys`` filesystem, and acquire information from there.
Thise information will then be stored in their respective directory on the ``acquire`` container.


Profiles
^^^^^^^^

*new in Acquire 3.11*

With the addition of volatile profiles ( used with ``--volatile-profile``) you can more easily add the volatile information.
There are currently three profiles ``extensive``, ``default`` and ``none``.
As with ``--profile``, the type of collected artifacts depend on the detected operating system.
``--volatile-profile`` can work together with ``--profile``, without any issue.

The following list shows the modules that belong to each ``volatile profile``.

.. code-block:: text

      default profile:
        windows: Netstat, WinProcesses, WinProcEnv, WinArpCache,
                 WinRDPSessions, WinDnsClientCache

      extensive profile:
        windows: Netstat, WinProcesses, WinProcEnv, WinArpCache,
                 WinRDPSessions, WinDnsClientCache
        linux  : Proc, Sys
        bsd    : Proc, Sys
        esxi   : Proc, Sys

Deployment
----------

Since ``acquire`` leverages Dissect to do its data collection, it can be used in different scenarios and ways.

One way is to use ``acquire`` on targets that are supported by ``dissect.target``, for example VMDK or E01 disk images.
This gives you a smaller forensic container for analysis. This can be useful in scenarios where you may have several thousand
virtual machine backups you want to analyze, but don't have the time (or storage) to fully copy them all. You can perform your
initial analysis and triage on the ``acquire`` container, and collect a copy of the full VM at a later stage if you require.

Besides various disk images, ``dissect.target`` also supports a ``local`` target, which is the host machine it's currently
running on. This is the default target for ``acquire``. For example, on Windows this means that ``\\.\PhysicalDrive0`` and
friends are opened and the filesystem on it is parsed using Dissect. On Linux systems this will be ``/dev/sda``, on ESXi
``/vmfs/devices/disks/vml.*``, etc. By parsing straight from the raw disk devices, we ensure we bypass any file locks and
filesystem drivers.

So how do you go about running ``acquire`` on a separate system? It's hardly practical to install Python and Dissect on a
compromised machine. At Fox-IT we have an internal solution for this, but fortunately there are also public options,
such as `PyOxidizer <https://pyoxidizer.readthedocs.io/en/stable/>`_ and `PyInstaller <https://pyinstaller.org/en/stable/>`_.
Unfortunately, however, neither support cross platform executable creation.

PyOxidizer
~~~~~~~~~~

PyOxidizer is a relatively new Python application packer that integrates heavily with Rust. It has a lot of exciting options
and functionality, at the cost of a fairly large executable size and complex configuration options.

A major benefit of PyOxidizer is that, by default, it runs all of its Python code completely from memory, no file extraction
necessary. This can result in the preservation of important filesystem artefacts.

Since ``dissect.target`` dynamically locates its plugins, we have to pre-generate a list of all plugins for it to work
when running in a self-contained executable.

Example usage of PyOxidizer with ``acquire``:

.. code-block:: console

    $ pip install pyoxidizer
    $ pyoxidizer init-config-file my-acquire-bin
    $ cd my-acquire-bin
    ## Edit pyoxidizer.bzl with your favourite text editor and see below for the minimal required changes
    $ target-build-pluginlist > /path/to/src/dissect.target/dissect/target/plugins/_pluginlist.py
    $ pyoxidizer build

The minimal required changes to be made to the ``make_exe()`` function in the ``pyoxidizer.bzl`` file are as follows:

.. code-block:: python

    policy.resources_location_fallback = "filesystem-relative:prefix"
    python_config.run_module = "acquire.acquire"
    exe.add_python_resources(exe.pip_install(["/path/to/src/dissect.target", "acquire"]))

This is just a very basic example. There are a lot more settings to tweak and optimizations to be made, but those are left
as an exercise to the reader.

PyInstaller
~~~~~~~~~~~

PyInstaller has been around for a long time and can be considered the de facto utility for packaging Python into
executables, for both legitimate and malicious purposes. It has a lot less options to play with than PyOxidizer, but
it's considerably easier to use and the resulting binaries are a lot smaller.

A major downside of PyInstaller is that you have to either ship multiple files or use the ``--onefile`` option, which
extracts files to a temporary directory on the filesystem. This can destroy forensic filesystem artefacts, so keep that
in mind when using PyInstaller.

Similar to PyOxidizer, we also have to pre-generate a list of plugins for PyInstaller.

Example usage of PyInstaller with ``acquire``:

.. code-block:: console

    $ pip install pyinstaller
    $ target-build-pluginlist > /path/to/src/dissect.target/dissect/target/plugins/_pluginlist.py
    $ pyinstaller /path/to/src/acquire/acquire.py --hidden-import dissect --collect-submodules dissect --onefile

This is again a very basic example. More optimized PyInstaller builds are left as an exercise to the reader.

Usage
-----

.. sphinx_argparse_cli::
    :module: acquire.acquire
    :func: main
    :prog: acquire
    :description:
    :hook:
