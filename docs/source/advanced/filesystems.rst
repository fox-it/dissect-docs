Filesystems
===========

In Dissect, filesystems are a lot more than *actual* filesystems on a disk. Because if you squint hard enough, almost
anything can be a filesystem! Dissect has various *real* filesystem implementations, such as
:doc:`/projects/dissect.ntfs/index` or :doc:`/projects/dissect.vmfs/index`, but Dissect also supports a lot of other
things that *resemble* a filesystem. For example, a ``.tar`` file, a directory on your local filesystem,
or even the API of a remote EDR agent can all be considered a type of filesystem.

The filesystem abstraction layer in ``dissect.target`` makes working with all of these different types of filesystems
quite easy. Most of the common use-cases, such as interacting with "normal" filesystems like NTFS or XFS, are already
supported, and when you require something exotic the APIs are usually sufficient to achieve your goal. The common
use-cases are automatically handled when using the various :doc:`tools </tools/index>` in ``dissect.target``, and when
you can use the :mod:`dissect.target.filesystem` API to achieve most other tasks. You can also choose to go one level
deeper and directly use the API from the individual Dissect libraries, such as :doc:`/projects/dissect.ntfs/index`.
Most of the APIs closely resemble the Python standard library, so they should look familiar if you're already
comfortable with Python.

.. seealso::

    Want to learn more about opening a filesystem in Python? Continue reading :ref:`here <advanced/api:filesystems>`.

    View all available filesystem implementations at :mod:`dissect.target.filesystems`.

There are some special types of "filesystem" that we will explain in a little more detail: the virtual filesystem and
the root filesystem.

Virtual filesystem
------------------

Sometimes you don't need to write a full fledged filesystem implementation and you just need a simple skeleton of one.
For example, when you want to map a file on your own local filesystem into a ``dissect.target`` filesystem, represent
the contents of a ``.zip`` or ``.tar`` file as a ``dissect.target`` filesystem, or even just a completely
fake and virtual file or directory. There would be a lot of duplicate boilerplate to achieve these simple tasks. For this
reason ``dissect.target`` has a :class:`~issect.target.filesystem.VirtualFilesystem` that should make most of these
tasks easy to do. Coincidentally it's also very useful in unit tests!

.. code-block:: python

    from io import BytesIO
    from dissect.target.filesystem import VirtualFile, VirtualFilesystem

    vfs = VirtualFilesystem()
    # Create some virtual directories
    vfs.makedirs("/here/be/directories")
    # Map a real file (``/etc/hostname``) on your local filesystem to ``/myhostname`` in the virtual filesystem
    vfs.map_file("/myhostname", "/etc/hostname")
    # Map an arbitrary file-like object to ``/path/to/some/file``
    vfs.map_file_fh("/path/to/some/file", BytesIO(b"content"))
    # Create a virtual symlink
    vfs.symlink("/path/to/some/", "dirlink")

    # Obtain a Path-like object to the root and print some info
    path = vfs.path()
    for entry in path.rglob("*"):
        print(str(entry))

    print(path.joinpath("/path/to/some/file").read_text())
    print(path.joinpath("/dirlink/file").read_text())
    print(path.joinpath("/myhostname").read_text())

.. seealso::

    View the API documentation and source of :class:`~dissect.target.filesystem.VirtualFilesystem`,
    :class:`~dissect.target.filesystem.VirtualFile` and :class:`~dissect.target.filesystem.VirtualDirectory` for more
    information.

    Browse the ``dissect.target`` source for more advanced usage examples of ``VirtualFilesystem``.

Root filesystem
---------------

In ``dissect.target`` we try to reconstruct the filesystem structure of a target as close as possible to how it would
look and work on a live system. This often means that we have to "mount" filesystems to some arbitrary paths, or
overlaying different filesystems on top of each other. To help with this we introduced the concept of a "root"
filesystem.

The root filesystem is a special type of virtual filesystem that allows multiple filesystems to overlay each other.
It allows for complex filesystem structures, such as instances where you have a "filesystem" that only contains
metadata, overlayed with one that contains file content for a select number of files. It also has some helper methods
for "mounting" other filesystems into the root filesystem.

.. seealso::

    View the API documentation and source of :class:`~dissect.target.filesystem.RootFilesystem` and
    :class:`~dissect.target.filesystem.RootFilesystemEntry` for more information.

Writing your own
----------------

There are a few methods of using your own filesystem implementation in ``dissect.target``:

* Specify the path to your implementation(s) using the ``DISSECT_PLUGINS`` environment variable.
* Specify the path to your implementation(s) using the ``--plugin-path`` argument with the various Dissect :doc:`/tools/index`.
* Add a new implementation in the ``dissect.target`` source tree at ``dissect/target/filesystems``.

The last method requires you to have a source checkout and working development setup of ``dissect.target``.
This is the recommended method if you intend to contribute your filesystem back to the project.

.. seealso::

    Read more about using your own modules in ``dissect.target`` at :ref:`advanced/api:loading your own modules`.

    Interested in developing for Dissect? Read more at :doc:`/contributing/developing`.

Regardless of which method you use, you can use the boilerplate below. Do keep in mind that the final line is only
required if you're using either of the ``DISSECT_PLUGINS`` or ``--plugin-path`` options!

.. code-block:: python

    from typing import BinaryIO

    from dissect.target.filesystem import Filesystem, FilesystemEntry
    from dissect.target.helpers import fsutil


    class MyFilesystem(Filesystem):
        # Specify a unique filesystem identifier
        __fstype__ = "myfs"

        def __init__(self, fh: BinaryIO, *args, **kwargs):
            # Do your initialization here, for example, initialize a parser:
            # self.fs = FSParser(fh)
            # Call ``super().__init__`` with the original file-like object and arguments
            super().__init__(fh, *args, **kwargs)
            # You can also do more complex initialization, view the NtfsFilesystem or TarFilesystem for examples

        def detect(fh: BinaryIO) -> bool:
            # Perform detection for your filesystem from a binary file-like object here
            # For example, check a specific magic superblock value
            raise NotImplementedError()

        def get(self, path: str) -> MyFilesystemEntry:
            # Retrieve a FilesystemEntry for the given path from your filesystem.
            raise NotImplementedError()


    class MyFilesystemEntry(FilesystemEntry):
        # This object represents a file on your filesystem
        def __init__(self, fs: Filesystem, path: str, entry: FilesystemEntry):
            # Perform additional initialization here if you need it
            super().__init__(fs, path, entry)

        def get(self, path: str) -> MyFilesystemEntry:
            # Retrieve a different filesystem entry relative to this one
            # In most filesystems it's more efficient to retrieve relative file entries instead of absolute ones
            raise NotImplementedError()

        def open(self) -> BinaryIO:
            # Open a file-like object for this filesystem entry
            raise NotImplementedError()

        def iterdir(self) -> Iterator[str]:
            # Iterate over all directory entries and yield all file names
            raise NotImplementedError()

        def scandir(self) -> Iterator[MyFilesystemEntry]:
            # Iteratie over all directory entries and yield all filesystem entries
            raise NotImplementedError()

        def is_file(self) -> bool:
            # Return whether this filesystem entry is a file
            raise NotImplementedError()

        def is_dir(self) -> bool:
            # Return whether this filesystem entry is a directory
            raise NotImplementedError()

        def is_symlink(self) -> bool:
            # Return whether this filesystem entry is a symbolic link
            raise NotImplementedError()

        def readlink(self) -> str:
            # Return the symbolic link target, if this is a symbolic link
            raise NotImplementedError()

        def stat(self) -> fsutil.stat_result:
            # Return stat information of this filesystem entry
            raise NotImplementedError()

        def lstat(self) -> fsutil.stat_result:
            # Return stat information of this filesystem entry, without resolving symlinks
            raise NotImplementedError()

    # This line is necessary if your filesystem is outside the ``dissect.target`` source tree!
    register(__name__, MyFilesystem.__name__, internal=False)

.. seealso::

    You can refer to the API documentation of the :class:`~dissect.target.filesystem.Filesystem`,
    :class:`~dissect.target.filesystem.FilesystemEntry` and
    :class:`fsutil.stat_result <dissect.target.helpers.fsutil.stat_results>` classes for more documentation on the
    methods referenced here.

If you are placing your implementation in the ``dissect.target`` source tree, you'll need to register your implementation.
Do this by opening ``dissect/target/filesystem.py`` and add your implementation to the bottom by using
:func:`~dissect.target.filesystem.register`:

.. code-block:: python

    register("myfilesystem", "MyFilesystem")
