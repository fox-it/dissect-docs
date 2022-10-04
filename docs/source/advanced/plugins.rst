Plugins
=======

The functionality that ``dissect.target`` provides can be separated into two categories:

* Interaction with target primitives, such as:

  * Disks
  * Volumes
  * Filesystems

* Interaction with high level target attributes and artefacts, such as:

  * Basic OS information (hostname, domain, version, users, etc...)
  * OS specific forensic artefacts (Event logs, bash history, registry artefacts, etc...)
  * Generic forensic artefacts (filesystem artefacts, browser history, etc...)

The former is what ``dissect.target`` provides as core functionality. High level interaction is provided by a
plugin system. This is also how you interact with a target using :doc:`/tools/target-query`.

On the technical side, a plugin is a Python class that exports a few of its methods to execute on a
:doc:`target </advanced/targets>`. To learn how to write your own plugin, skip ahead to
:ref:`advanced/plugins:writing your own`.

Type of plugins
---------------

There are a couple of plugin types that you should know about. The main difference between them is how they can be used.

OS plugins
~~~~~~~~~~

OS plugins are very important in ``dissect.target`` and OS detection is an important step in the
:ref:`initialisation of a target <advanced/targets:initialisation>`. OS plugins are the first layer between the target
primitives and the rest of the plugins. They are responsible for mounting filesystems to their correct location in the
:ref:`advanced/filesystems:root filesystem` and for performing any additional OS initialisation steps. Additionally,
they provide basic OS specific information, such as the ``hostname``, ``version``, and ``users`` of a target.

Let's compare the initialisation of :class:`~dissect.target.plugins.os.windows._os.WindowsPlugin` and
:class:`~dissect.target.plugins.os.unix.esxi._os.ESXiPlugin`. The ``WindowsPlugin`` detects the system volume, mounts the
system volume to ``sysvol``, and the rest of the volumes to the correct drive letters. There is not much to the
initialisation of a Windows target. The ``ESXiPlugin`` on the other hand, goes through an elaborate process of rebuilding
the ESXi root filesystem from ``.tar`` files, parsing configuration, mounting volumes, and creating symlinks according to
complex rules. The end result is that from that point onward, any other plugin can interact with an ESXi targets'
filesystem as if it was a live system because it was accurately reconstructed.

Internal plugins
~~~~~~~~~~~~~~~~

Internal plugins provide functionality for (surprise!) internal use. This means that they are unavailable through
:doc:`/tools/target-query` and only callable from within Python.

These plugins generally provide functionality that aids other plugins or makes plugin development easier. For example,
consider a plugin that provides environment variable expansion, or one that allows you to calculate UTC timestamps from
the local system time zone information.

One very important internal plugin that warrants its own documentation is the Windows registry plugin.

Windows Registry
^^^^^^^^^^^^^^^^

The Windows registry is a vital part of the Windows operating system, but also vital to the field of digital forensics.
It contains a lot of interesting forensic artefacts, in addition to a lot of important information that is necessary
to correctly interpret a Windows target. For example, configured log file locations, which codepage is in use,
what time zone is configured, which drive letter belongs to which volume, and much more.

Because the registry is so important, there's a special internal plugin in ``dissect.target`` to make interacting with it
a breeze. Among other things, it has support for different sources of registry data, such as:

* Binary ``regf`` hives
* Hives imported from ``.reg`` files
* Virtual hives

It also supports multiple dimensions of the same hive (active, ``REGBACK`` or replayed hives, multiple ``ControlSet`` keys).
All the hives are mapped in a similar structure as Windows does, meaning registry paths like ``HKLM\SOFTWARE`` or
``HKEY_CURRENT_USER`` work just as you expect them to.

Let's look at this last concept in a bit more detail and take ``HKEY_CURRENT_USER`` as an example. On a live Windows
system, things like ``HKEY_CURRENT_USER`` and ``CurrentControlSet`` map to a single key. This makes sense, because on
a live system you only have one current user, and only one current control set. However, when performing digital
forensics, you want as much data as possible. Maybe a setting was changed in an older control set and isn't visible
anymore in the "current" control set? Maybe a persistency method exists in a ``REGBACK`` version of a hive but no
longer in the active hive? To make working with this concept easier from an analysis and plugin development point
of view, we allowed a registry key or value to exist multiple times.

``HKEY_CURRENT_USER`` is really just a little bit of syntactic sugar around this concept. This allows for easy
analysis and plugin development, since you don't have to iterate user hives yourself, and can just use ``HKCU`` instead.
Underwater it will iterate over all the user hives for you, and simply return all of the keys that exist within those
hives. So, a query for ``HKCU\Software\Microsoft\Windows\CurrentVersion\Run`` returns all the possible run key entries
of all the users that have registry hives.

Let's assume we have a fully initialised Windows target on variable ``t``. Here are some examples of how you would
interact programmatically with the registry of the target:

.. code-block:: python

    # Access a single key
    t.registry.key("HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")

    # Access a single subkey
    t.registry.subkey("HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList", "S-1-5-18")

    # Access a single value
    t.registry.value("HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion", "CSDVersion")

    # Iterate over all possible keys (recommended)
    for key in t.registry.keys("HKCU\\Software\\Microsoft\\Office"):
        for subkey in key.subkeys():
            print(subkey.subkeys())

There is also the :doc:`/tools/target-reg` utility to easily interact with the registry of a Windows target from the
command line, which essentially is a small utility around the registry plugin!

.. seealso::

    For more information, please refer to the documentation of
    :class:`~dissect.target.plugins.os.windows.registry.RegistryPlugin`.

Artefact plugins
~~~~~~~~~~~~~~~~

Most other plugins in ``dissect.target`` are regular plugins, or plugins that parse artefacts. For convenience we'll
call these artefact plugins. These types of plugins are the ones you generally interact with when using
:doc:`/tools/target-query` and generally parse some piece of data from a target and return some kind of output.

Namespace plugins
~~~~~~~~~~~~~~~~~

Sometimes it makes sense to "namespace" your plugin. For example, the Windows System Resource Usage (SRU) database
has multiple tables that are of interest. We want to make a distinction between the different tables and thus have
separate plugin functions for parsing and returning those. However, we also want an easy option to parse *all* of
the SRU tables at once.

This is where namespace plugins are useful. It allows us to nicely separate the different table parsing functions into
different plugins such as ``sru.network_data`` and ``sru.application``, while simultaneously allowing us to execute
all of the namespace functions by simply calling ``sru``.

Caching
-------

During investigations it might be useful to cache plugin output for performance reasons. ``dissect.target`` has some
primitive file-based caching to speed up future executions of the same plugin. To configure caching, place a file
called ``.targetcfg.py`` in the same directory as your target files with the following content:

.. code-block:: python

    CACHE_DIR = "/path/to/cache/directory"

Having this file in the same directory as your targets will cause the cache for those targets to be written to the
given directory. You can also have different configurations for different targets, as the parent directories are
traversed to find ``.targetcfg.py``:

.. code-block:: text

    /t/
    ├── domain_a
    │   ├── EXAMPLE02.tar       # Uses the .targetcfg.py from /t/domain_a
    │   └── .targetcfg.py
    ├── domain_b
    │   ├── EXAMPLE03.vma       # Uses the .targetcfg.py from /t/domain_b
    │   └── .targetcfg.py
    ├── domain_c
    │   └── EXAMPLE04.qcow2     # Uses the .targetcfg.py from /t/
    ├── EXAMPLE01.E01           # Uses the .targetcfg.py from /t/
    └── .targetcfg.py

You can influence caching behaviour with the ``--no-cache``, ``--only-read-cache`` and ``--rewrite-cache`` arguments
in :doc:`/tools/target-query` or by setting the ``IGNORE_CACHE``, ``ONLY_READ_CACHE``, or ``REWRITE_CACHE`` environment
variables to either ``0`` or ``1``.

Writing your own
----------------

Writing your own plugin is pretty easy. There are a few methods of using your own plugin in ``dissect.target``:

* Specify the path to your plugin(s) using the ``DISSECT_PLUGINS`` environment variable.
* Specify the path to your plugin(s) using the ``--plugin-path`` argument with the various Dissect :doc:`/tools/index`.
* Add a new plugin in the ``dissect.target`` source tree at ``dissect/target/plugins``.

The last method requires you to have a source checkout and working development setup of ``dissect.target``.
This is the recommended method if you intend to contribute your plugin back to the project.

.. seealso::

    Read more about using your own modules in ``dissect.target`` at :ref:`advanced/api:loading your own modules`.

Either way, you'll need to write your plugin. Here's an example which explains a lot of concepts:

.. literalinclude:: ../../../submodules/dissect.target/dissect/target/plugins/general/example.py

Output types
~~~~~~~~~~~~

Plugins can have a couple types of outputs:

* ``default``

  * Basic Python types such as ``int``, ``str``, ``list``, etc. Mostly useful for simple or internal plugins.

* ``record``

  * Records are the recommended output for most artefact plugins.

* ``yield``

  * Yield basic Python types, such as a generator of ``str`` of a human-readable filesystem timeline.

* ``none``

  * No output or returns ``None``, useful when the plugin prints something on its own (such as the plugin that lists
    which plugins are available).

Records
~~~~~~~

Records are the main data format used by plugins to output information. If you don't yet know what records are, read a
short explanation in the :ref:`overview <overview/index:records>`. The important thing to know in the context of writing
your own plugin is that you need to write a record descriptor that describes what fields your record has.

The following field types are available:

* ``boolean``
* ``bytes``
* ``datetime``
* ``digest``
* ``dynamic``
* ``filesize``
* ``float``
* ``net.ipaddress``
* ``net.ipnetwork``
* ``record``
* ``string``
* ``uint16``
* ``uint32``
* ``unix_file_mode``
* ``uri``
* ``varint``

You can also create a list of any of these types by specifying the type as ``type[]``, so for example ``string[]`` for
a list of strings.

Within ``dissect.target``, there are a couple of helpers available for working with records. Most notable is the
:data:`~dissect.target.helpers.record.TargetRecordDescriptor`.

Historically, we'd manually add a couple of common fields to each record, such as the hostname or domain of a target.
Sometimes errors or typos snuck in, so we standardized this by introducing the ``TargetRecordDescriptor``. You can
already see its usage in the example plugin above, but the basic idea is that instead of manually passing the
hostname and domain, you pass a target as ``_target=target`` keyword argument, and the ``TargetRecordDescriptor``
will take care of the rest.

There are two additional so-called record extensions:
:class:`~dissect.target.helpers.descriptor_extensions.RegistryRecordDescriptorExtension` and
:class:`~dissect.target.helpers.descriptor_extensions.UserRecordDescriptorExtension`. The use of these is also
demonstrated in the example plugin above.
