acquire
=======

``acquire`` is a tool to quickly gather forensic artifacts from disk images or a live system into a lightweight container.
This makes ``acquire`` an excellent tool to, among others, speed up the process of digital forensic triage.
``acquire`` uses ``dissect`` to gather forensic artifacts from the raw disk, if possible.

``acquire`` gathers artifacts based on modules. These modules are paths or globs on a filesystem which acquire attempts to gather.
Multiple modules can be executed at once, which have been collected together inside a profile.
These profiles (used with ``--profile``) are  ``full``, ``default``, ``minimal`` and ``none``.
Depending on what operating system gets detected, different artifacts are collected.

The most basic usage of ``acquire`` is as follows:

.. code-block:: console

    $ sudo acquire

The tool requires administrative access to read raw disk data instead of using the operating system for file access.
However, there are some options available to use the operating system as a fallback option. (e.g ``--fallback`` or ``--force-fallback``)

The following list shows the modules belonging to each ``profile``.

.. code-block:: text

    full profile:
      windows: AV, ActivitiesCache, Appcompat, BITS, DHCP, DNS,
               Drivers, ETL, EventLogs, History, Misc, NTDS,
               NTFS, Prefetch, QuarantinedFiles, Recents,
               RecycleBin, Registry, RemoteAccess, Syscache,
               Tasks, WBEM, WindowsNotifications
      linux  : Etc, Boot, Home, Var
      bsd    : Etc, Boot, Home, Var, BSD
      esxi   : Bootbanks, ESXi, VMFS
      osx    : Etc, Home, Var, OSX, History

    default profile:
      windows: NTFS, EventLogs, Registry, Tasks, ETL, Recents,
               RecycleBin, Drivers, Prefetch, Appcompat,
               Syscache, WBEM, AV, BITS, DHCP, DNS, Misc,
               RemoteAccess, ActivitiesCache
      linux  : Etc, Boot, Home, Var
      bsd    : Etc, Boot, Home, Var, BSD
      esxi   : Bootbanks, ESXi, VMFS
      osx    : Etc, Home, Var, OSX

    minimal profile:
      windows: NTFS, EventLogs, Registry, Tasks, Prefetch,
               Appcompat, Misc
      linux  : Etc, Boot, Home, Var
      bsd    : Etc, Boot, Home, Var, BSD
      esxi   : Bootbanks, ESXi
      osx    : Etc, Home, Var, OSX


Profile ``none`` is a special case where no module gets collected.
This profile, is used in combination with ``--dir``, ``--file`` or ``--glob`` to collect specific paths from a target.
These arguments do the following:

* ``--dir``: Collects a directory recursively.
* ``--file``: Collects one specific file.
* ``--glob``: Collects any file or directory that matches the specific glob pattern. (e.g ``/path*/test`` would collect for example ``/path1/test`` and ``/path_to_other_test_file/test``)

You can specify these arguments multiple times for every file, directory or glob you want to collect.

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
