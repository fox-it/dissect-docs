Loaders
=======

Loaders are a key component of what makes ``dissect.target`` work. They are responsible for mapping any kind of source
data into something that ``dissect.target`` understands. Loaders can be incredibly complex or incredibly simple,
depending on what you are trying to achieve.

Oftentimes, your data is not in a directly usable state or it's split over multiple files that would make more sense
to use as a single entity, but needs some molding to properly use it. A loader can be seen as a preprocessor of this
source data, shaping it into something more useful. All the processing happens transparently or in-memory.

For example:

* A loader for ``.vmx`` (VMware VM metadata) files parses the metadata and loads all of the discovered ``.vmdk``
  (VMware virtual disk) files.
* A loader for ``.vbox`` (Virtual Box metadata) and ``.vmcx`` (Hyper-V metadata) files does the same as the loader
  for ``.vmx``, but for ``.vdi``, ``.vhd`` and ``.vhdx`` files.
* A loader for ``.vma`` (Proxmox VM backup) files can parse the backup and add each enclosed virtual disk stream
  as a separate disk, without having to extract the ``.vma`` file.
* A loader for :doc:`/tools/acquire` tar files can map all files to virtual in-memory filesystems.
* A loader for an EDR agent can use the live API to provide virtual filesystems and registry hives.
* A loader for roaming profile managers can parse profile data and map files to a virtual in-memory filesystem
  and registry keys to a virtual in-memory registry hive.
* A loader for iTunes backups can parse the metadata and map all the enclosed files into a virtual in-memory
  filesystem, providing transparent decryption for any file reads.

These are just some examples of the loaders currently available in ``dissect.target``, but more are added as support
grows or new use-cases are encountered.

This doesn't mean that ``dissect.target`` only works with these types of files, however. As mentioned, a loader can
be seen as a preprocessor; a way to work with more complex data or data that is scattered over multiple files.
A target is usually a single file, but a loader for that single file can pull in as many files as it needs.

Using ``dissect.target`` on a single (supported) file, such as a ``.vmdk`` or ``.E01`` works without needing a
loader. In fact, the file support for ``.E01`` actually cheats a little by pulling in more files (the other
``.E**`` part files) without needing a loader. This is not by accident, as a ``.E01`` file is a completely
self-contained disk container, so it's possible to address it as such. In contrast, a ``.vma`` or ``.vmx`` file can
produce multiple disk containers, so a loader is required to correctly open each disk container.
It also allows for a separate tool that only consumes the :doc:`/advanced/containers` API to support opening
``.E01`` files.

Writing your own
----------------

There are a few methods of using your own loader in ``dissect.target``:

* Specify the path to your implementation(s) using the ``DISSECT_PLUGINS`` environment variable.
* Specify the path to your implementation(s) using the ``--plugin-path`` argument with the various Dissect :doc:`/tools/index`.
* Add a new implementation in the ``dissect.target`` source tree at ``dissect/target/loaders``.

The last method requires you to have a source checkout and working development setup of ``dissect.target``.
This is the recommended method if you intend to contribute your loader back to the project.

.. seealso::

    Read more about using your own modules in ``dissect.target`` at :ref:`advanced/api:loading your own modules`.

    Interested in developing for Dissect? Read more at :doc:`/contributing/developing`.

Regardless of which method you use, you can use the boilerplate below. Do keep in mind that the final line is only
required if you're using either of the ``DISSECT_PLUGINS`` or ``--plugin-path`` options!

.. code-block:: python

    from pathlib import Path
    from typing import TYPE_CHECKING

    from dissect.target.loader import Loader, register

    if TYPE_CHECKING:
        from dissect.target import Target


    class MyLoader(Loader):
        @staticmethod
        def detect(path: Path) -> bool:
            raise NotImplementedError()

        def map(self, target: Target) -> None:
            raise NotImplementedError()


    # This line is necessary if your loader is outside the ``dissect.target`` source tree!
    register(__name__, MyLoader.__name__, internal=False)

In the ``detect()`` method you can place detection logic that determines if your loader is compatible with the
given ``path``, simple return ``True`` if it is and ``False`` if it isn't.  Please note that ``path`` doesn't
necessarily have to be a path to an actual file on your local filesystem. It can also be a path on a filesystem
of another target (a ``TargetPath``, more information in :doc:`/advanced/filesystems`).  It's also possible to
parse the path as a URI, the :class:`~dissect.target.loaders.local.LocalLoader` does this for example.

Keep this in mind when writing your own loader, and steer clear of any OS specific APIs such as those from the
Python ``os`` or ``os.path`` module, unless explicitly intended.

If your loader is compatible with a given path, it will be instantiated with the ``path`` as an argument.
If you want, you can provide additional initialization logic in the ``__init__`` function by overriding it:

.. code-block:: python

    class MyLoader(Loader):
        def __init__(self, path: Path):
            # Your additional initialization logic here
            super().__init__(path)

The next important method to implement is the ``map()`` method. This is the meat and bones of your loader.
Here you can do all the crazy logic you want for whatever it is you want to load into a ``Target``.
Common use-cases include opening :doc:`/advanced/containers` or mapping things into various (virtual)
:doc:`/advanced/filesystems`. You can look at other loaders as an example or explore the documentation for
other various Dissect components to discover all the possibilities.

One important detail to keep in mind is that in your ``map()`` method, the target is in an empty state.
There are no disks, volumes or filesystems yet (you're adding them, after all), and there's no operating
system information loaded yet. Another important detail is to understand that you generally don't have to do
things like volume or filesystem discovery yourself, unless you specifically require so in your loader.
If you add a disk, things like volume and filesystem happen automatically as the ``Target`` object gets
initialized. Read more about this process at :ref:`Target initialization <advanced/targets:initialisation>`.

.. seealso::

    You can refer to the API documentation of the :class:`~dissect.target.loader.Loader` class for more documentation
    on the methods referenced here.

If you are placing your loader in the ``dissect.target`` source tree, you'll need to register your loader.
Do this by opening ``dissect/target/loader.py`` and add your loader to the bottom by using
:func:`~dissect.target.loader.register`:

.. code-block:: python

    register("myloader", "MyLoader")
