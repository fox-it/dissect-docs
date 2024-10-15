Targets
=======

Targets (or target) is the terminology we use for the type of source data supported by ``dissect.target``. It includes
anything that can, one way or another, be used to describe a certain state of a system.

Some examples include:

* Raw disk images, virtual disks (``.vmdk``, ``.vhdx``, etc) and evidence containers (``.E01``)
* Virtual machine descriptor files (``.vmx``, ``.vmcx``, etc)
* Local live systems (``\\.\PhysicalDrive0``, ``/dev/sda``)
* Forensic packages such as ``.tar`` archives created by :doc:`/tools/acquire` or KAPE output directories
* ... and more

It's important to be aware of the difference between virtual machine descriptor (like ``.vmx``) and virtual disk
(like ``.vmdk``) files. For example, when using a ``.vmdk`` with Dissect, only that VMDK will be loaded, but when
using a ``.vmx``, all the ``.vmdk`` files described in that VMX file will be loaded instead. This ensures that systems
with multiple virtual disks work as intended. A ``.vmx`` file and ``.vmdk`` file are thus both valid targets. Keep this
in mind when working with investigative data.

On the technical side, everything eventually gets loaded into a ``Target`` Python object. The following sections
will go into more detail on how this object works. This is generally only useful information if you're looking to
interact with a target from your own Python code or writing a plugin for ``dissect.target``.

The ``Target`` object
---------------------

The :class:`~dissect.target.target.Target` class is your primary interaction point in ``dissect.target``. It represents
some system in some specific state, loaded from some target files. Any interaction you want to do with that system is
done through the ``Target`` class.

Conceptually a target consists of one or more :doc:`disks </advanced/containers>`, :doc:`volumes </advanced/volumes>`
and :doc:`filesystems </advanced/filesystems>`, which can be modified or added by :doc:`/advanced/loaders`.
These items are available as attributes on a ``Target`` instance we've named ``t`` at:

* ``t.disks``
* ``t.volumes``
* ``t.filesystems``

The next important attribute to know about is ``Target.fs``, which is the
:ref:`root filesystem <advanced/filesystems:root filesystem>`. This object behaves like any other filesystem in
``dissect.target``, but exists to allow other filesystems to be mounted at arbitrary paths or drive letters within
the context of a ``Target``. Use this when you need to interact with "the filesystem" of a target.

Finally, there are the :doc:`/advanced/plugins`. Plugins are functions that can be executed on a target. They can be as
simple as reading the hostname from ``/etc/hostname``, or as advanced as parsing a specific artefact like the
Windows event log.

Plugins are dynamically made available on the ``Target`` object. For example, if you wanted to run the ``evtx`` plugin
on a ``Target`` instance named ``t``, you would do ``t.evtx()``, which will:

* Check if the ``evtx`` function is already cached, otherwise perform a lookup which will:

  * Find a plugin that exports the ``evtx`` function and see if it's compatible.
  * Cache it and register it on the ``Target`` instance ``t``, it is now available as ``t.evtx``.

* If the plugin function is marked as a ``property``, it will behave like a Python ``@property``.
* If it's a function, calling it (``t.evtx()``) will execute the plugin function.

.. seealso::

    For more information on how plugins work, please read their documentation at :doc:`/advanced/plugins`.

    To learn more about the ``Target`` object, it's recommended to read either the :class:`~dissect.target.target.Target`
    class documentation or the `source code <https://github.com/fox-it/dissect.target/blob/main/dissect/target/target.py>`_.

Initialisation
~~~~~~~~~~~~~~

``Target`` initialisation usually starts with finding a :doc:`loader </advanced/loaders>` for a target, unless you're
:ref:`manually opening a target <advanced/targets:manually opening a target>`. If no compatible loader is found, the
default behaviour is to treat the target path as a container and add it as a disk.
After all of the discovered disks, volumes and/or filesystems are added by a loader (or the default behaviour), the
``Target`` object will continue initialisation.

Initialisation roughly consists of the following steps:

* Iterate ``Target.disks``.

  * Perform volume discovery using :func:`volume.open() <dissect.target.volume.open>` and add to ``Target.volumes``.
  * Add disk as a raw volume if no additional volumes were discovered.

* Iterate ``Target.volumes``.

  * Discover and open logical volume managers using :func:`volume.open_lvm() <dissect.target.volume.open_lvm>` and
    add discovered logical volumes to ``Target.volumes``.
  * Discover and open encrypted volumes using :func:`volume.open_encrypted() <dissect.target.volume.open_encrypted>` and
    add discovered and decrypted volumes to ``Target.volumes``.
  * Perform filesystem discovery using :func:`filesystem.open() dissect.target.filesystem.open>` and add discovered
    filesystems to ``Target.filesystems``.

* Basic initialisation is now done, OS detection still has to happen but that can fallback to a "no-op" OS plugin,
  leaving you able to interact with just the disks, volumes and filesystems.
* Find and iterate over all :ref:`advanced/plugins:os plugins` to find the most specific OS.

  * Subclasses of different OS plugins are considered "more specific", so e.g.
    :class:`~dissect.target.plugins.os.unix.debian._os.DebianPlugin` is more specific than
    :class:`~dissect.target.plugins.os.unix._os.LinuxPlugin`.

* OS initialisation is performed, this is can be super simple or extremely complex. Generally it consists of:

  * All the filesystems are mounted at their correct mount points in the
    :ref:`root filesystem <advanced/filesystems:root filesystem>`.
  * Optional additional OS specific parsing or initialisation is performed.

* The ``Target`` is now fully initialised.

Manually opening a target
~~~~~~~~~~~~~~~~~~~~~~~~~

There are multiple ways to open a ``Target`` object. The recommended way to open a single target is to use the
:func:`Target.open() <dissect.target.target.Target.open>` method, or
:func:`Target.open_all() <dissect.target.target.Target.open_all>` to open multiple targets from a single path. These
will return (or yield) a fully initialized and loaded ``Target`` object for you to start interacting with.

You can also opt to manually open a target. This can be useful when you're writing some code that needs to modify
attributes, or manually add things like filesystems. For example, a recovery script that scrapes for a filesystem
that may have had its superblock or ``$BOOT`` destroyed:

.. code-block:: python

    from dissect.target import Target

    t = Target()
    t.filesystems.add(recover_filesystem())
    t.apply()

    print(t.hostname)


Targets in targets
------------------


Dissect also supports the concept of targets within targets, referred to as child targets.
Child targets are especially useful for dealing with hypervisors. With the child target feature
you can query virtual machines that are running on a host. Because of the way Dissect handles the
underlying data streams you can query these virtual machines regardless of the locks the host
operating system has on these files. It is even possible to explore the contents of the child targets
using ``target-shell`` just like regular targets!

.. hint::

    Learn more about child targets :doc:`here </advanced/children>`.
