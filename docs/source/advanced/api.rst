Python API
==========

This page really only exists to attract the attention of those looking for how to use Dissect programmatically.
There's nothing special you need to do, because Dissect is designed to be API first, tool second!
No longer are you limited with what a single-purposes script or executable does, you get complete freedom to use
any component or parser in Dissect however you see fit.

This does make explaining exactly *what* you can do with the Python API difficult because, well, it's everything.
To not leave you to discover *everything* on your own, we'll describe how to use some of the core components of
Dissect from your own Python code.

Containers
----------

Interacting with disk images in different shapes and sizes is a common task in digital forensics. In Dissect we use the
term "container" for any data format that *contains* a raw disk or volume within it. For example, a DD image is a
raw or plain container, but a ``.E01`` file is an EWF container. Likewise, ``.vmdk`` and ``.vhdx`` files are
respectively VMDK and VHDX virtual disk containers.

In Dissect we like to keep things simple, so there's no complex API for working with containers. If you know how
to work with a binary file in Python, you know how to work with a container. Let's open a container using
:func:`container.open() <dissect.target.container.open>`:

.. code-block:: python

    import io

    from dissect.target import container

    fh = container.open("/path/to/file.vmdk")
    print(fh.read(512))
    fh.seek(-512, io.SEEK_END)
    print(fh.read(512))

That's it! ``fh`` will behave like any other Python file-like object. This means it has all the methods you already
know when working with binary files in Python and that it's automatically compatible with any API that accepts a
file-like object.

You can also use specific container implementations by using them directly. For example, to open a QCOW2 file, you can use:

.. code-block:: python

    from dissect.target.containers.qcow2 import QCow2Container

    with open("/path/to/file.qcow2", "rb") as fh:
        disk = QCow2Container(fh)

        print(disk.read(512))


.. seealso::

    View all available container implementations at :mod:`dissect.target.containers`.

    To learn more about containers, continue reading at :doc:`/advanced/containers` or read the API documentation of
    the :mod:`dissect.target.container` module.

Volumes
-------

After opening a disk, you usually want to parse individual volumes on that disk. This is where the volume parsers of
Dissect come into play.

Similarly, like containers, there is no complex API to working with volumes. If you know how to work with a binary file
in Python, you know how to work with volumes. Let's open a volume system using
:func:`volume.open() <dissect.target.container.open>` and list some volumes from a disk:

.. code-block:: python

    from dissect.target import container, volume

    # First open a disk. We use a container in this example but this can also be
    # any file you open with ``open("/path/to/file.dd", "rb")``.
    disk = container.open("/path/to/file.vmdk")
    # Opening a volume system (vs) is as easy as passing the file-like object.
    vs = volume.open(disk)

    for volume in vs.volumes:
        # The Volume object has some useful attributes...
        print(f"Volume #{volume.number} ({volume.name}, {volume.size} bytes)")
        # ... but otherwise also behaves like a file-like object.
        print(volume.read(512))
        print()

Again, volumes are just like any other file-like objects. They have some additional useful attributes, but for all
intents and purposes it's a file-like object.

.. seealso::

    View all available volume system implementations at :mod:`dissect.target.volumes`.

    To learn more about volume systems and volumes (including logical and encrypted volume systems), continue reading
    at :doc:`/advanced/volumes` or read the API documentation of the :mod:`dissect.target.volume` module.

Filesystems
-----------

The next step when interacting with host data is the filesystem. Once again, Dissect tries to make this as painless
as possible by adhering as closely to the standard Python functions as possible. Opening a filesystem is very easy using :func:`filesystem.open() <dissect.target.filesystem.open>`:

.. code-block:: python

    from dissect.target import container, filesystem, volume

    # First open a disk and some volumes.
    # Again, this can be skipped if you directly open a file with a filesystem on it.
    disk = container.open("/path/to/file.vmdk")
    vs = volume.open(disk)
    # Open a filesystem by passing it a file-like object, in this case a volume we opened in the previous step.
    fs = filesystem.open(vs.volumes[0])
    # There are functions similar to ``os.path`` available on the filesystem object itself...
    print(fs.listdir("/"))
    # Opening a file is just another file-like object.
    print(fs.get("file.txt").open().read(512))
    # Or a (mostly) compatible ``pathlib.Path`` object!
    path = fs.path("/")
    print(list(path.joinpath("some dir").iterdir()))
    print(fs.path.joinpath("file.text").read_text())

Just like containers, you can open specific filesystems by importing and using them directly.

.. code-block:: python

    from dissect.target.filesystems.ntfs import NtfsFilesystem

    with open("/path/to/volume.dd", "rb") as fh:
        fs = NtfsFilesystem(fh)
        print(fs.listdir("/"))

As shown in the examples, there are two main ways of interacting with a filesystem: using ``os.path``-like functions
on the :class:`~dissect.target.filesystem.Filesystem` and :class:`~dissect.target.filesystem.FilesystemEntry` classes,
or by using the (mostly) ``pathlib.Path`` compatible :class:`~dissect.target.helpers.fsutil.TargetPath`. The latter
is recommended for new code.

.. seealso::

    View all available filesystem implementations at :mod:`dissect.target.filesystems`.

    To learn more about filesystems (including virtual filesystems, the root filesystem, and ``TargetPath``), continue
    reading at :doc:`/advanced/filesystems` or read the API documentation of the :mod:`dissect.target.filesystem` module.

Targets
-------

Targets are what glues everything together. This is how you interact with a "full" system, from accessing raw disks
and volumes, to interpreting and parsing OS specific artefacts. To open one or more targets, you can use the
:func:`Target.open() <dissect.target.target.Target.open>` or
:func:`Target.open_all() <dissect.target.target.Target.open_all>` methods:

.. code-block:: python

    from dissect.target import Target

    # Open a single target.
    t = Target.open("/path/to/target.vmx")
    # Open multiple targets.
    for t in Target.open_all("/path/to/a/directory/with/targets"):
        print(t.hostname)

You can also manually create a :class:`~dissect.target.target.Target` object and manually add disks, volumes or
filesystems:

.. code-block:: python

    from dissect.target import Target

    t = Target()
    t.disks.add(open_disk())
    # And/or
    t.volumes.add(open_volume())
    # And/or
    t.filesystems.add(open_filesystems())
    # Calling .apply() will start loading the target.
    t.apply()
    # Execute a plugin function, in this case the `hostname` function from the OS plugin...
    print(t.hostname)
    # ... or the `runkeys` plugin function, assuming this was a Windows target.
    for entry in t.runkeys():
        print(entry)

.. seealso::

    To learn more about targets, continue reading at :doc:`/advanced/targets`. To learn more about plugins, continue
    reading at :doc:`/advanced/plugins`.

Loading your own modules
------------------------

There are a couple of ways you can add your own modules to ``dissect.target``. You can choose from the following options:

* Specify the path to your module(s) using the ``DISSECT_PLUGINS`` environment variable.
* Specify the path to your module(s) using the ``--plugin-path`` argument with the various Dissect :doc:`/tools/index`.
* Add a new module in the ``dissect.target`` source tree at the correct respective directory.

For regular tool usage or when testing a new functionality, either the environment variable or command line argument
options are recommended. These options will allow you to specify directories or individual files. Once you intend to
contribute your module back to the Dissect project, you'll have to move it into the ``dissect.target`` source tree.

For example, you could add ``DISSECT_PLUGINS=~/dissect-plugins`` to your ``.bashrc`` (or equivalent of your shell) to
always load addtional modules from ``~/dissect-plugins``. Or test out a new plugin and loader using
``target-query --plugin-path ./myplugin.py --plugin-path ./myloader.py``.

.. note::

    For more information about developing for Dissect, please continue reading at :doc:`/contributing/developing`.

    Learn how to write your own :ref:`loader <advanced/loaders:writing your own>`,
    :ref:`container <advanced/containers:writing your own>`, :ref:`volume system <advanced/volumes:writing your own>`,
    :ref:`filesystem <advanced/filesystems:writing your own>` or :ref:`plugin <advanced/plugins:writing your own>` by
    referring to each respective documentation page.

Other Dissect libraries
-----------------------

Dissect consists of a lot of libraries. For more details and usage examples on those libraries, please refer to
the specific project page under :doc:`/projects/index` or the API documentation at :doc:`/api/index`.
