Containers
==========

Containers in ``dissect.target`` are the abstraction layer for anything that looks (or should look) like a raw disk.
For example, VMware VMDK or Microsoft Hyper-V VHD(X) files may be custom file formats, but in the end these are merely *containers* of the raw disk(s) inside.

The container abstraction layer in ``dissect.target`` makes working with these different disk containers easy. Once
opened, all containers behave as a binary file-like object. This means that there's no special API for working with
containers, if you know how to read from a file in Python, you'll know how to read from a container.

.. seealso::

    To see how to open a container in Python, continue reading :ref:`here <advanced/api:containers>`.

    View all available container implementations at :mod:`dissect.target.containers`.

Writing your own
----------------

There are a few methods of using your own container implementation in ``dissect.target``:

* Specify the path to your implementation(s) using the ``DISSECT_PLUGINS`` environment variable.
* Specify the path to your implementation(s) using the ``--plugin-path`` argument with the various Dissect :doc:`/tools/index`.
* Add a new implementation in the ``dissect.target`` source tree at ``dissect/target/containers``.

The last method requires you to have a source checkout and working development setup of ``dissect.target``.
This is the recommended method if you intend to contribute your container back to the project.

.. seealso::

    Read more about using your own modules in ``dissect.target`` at :ref:`advanced/api:loading your own modules`.

    Interested in developing for Dissect? Read more at :doc:`/contributing/developing`.

Regardless of which method you use, you can use the boilerplate below. Do keep in mind that the final line is only
required if you're using either of the ``DISSECT_PLUGINS`` or ``--plugin-path`` options!

.. code-block:: python

    import io
    from pathlib import Path
    from typing import BinaryIO, Union

    from dissect.target.container import Container, register


    class MyContainer(Container):
        def __init__(self, fh: Union[BinaryIO, Path], *args, **kwargs):
            # Do your initialization here, for example, initialize a parser:
            # self.vmdk = VMDK(fh)
            # Call ``super().__init__`` with the original file-like object(s) and the container size
            super().__init__(fh, size, *args, **kwargs)

        @staticmethod
        def detect_fh(fh: BinaryIO, original: Union[list, BinaryIO]) -> bool:
            # Perform detection for your container from a binary file-like object here
            # For example, check a specific magic header value
            raise NotImplementedError()

        @staticmethod
        def detect_path(path: Path, original: Union[list, BinaryIO]) -> bool:
            # Perform detection for your container from a Path object here
            # For example, check a specific file extension
            raise NotImplementedError()

        def read(self, length: int) -> bytes:
            # Perform a file read for ``length`` amount of bytes
            raise NotImplementedError()

        def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
            # Perform a file seek here
            raise NotImplementedError()

        def tell(self) -> int:
            # Perform a file tell here
            raise NotImplementedError()

        def close(self) -> None:
            # Perform any close actions here
            pass


    # This line is necessary if your container is outside the ``dissect.target`` source tree!
    register(__name__, MyContainer.__name__, internal=False)

.. seealso::

    You can refer to the API documentation of the :class:`~dissect.target.container.Container` class for more
    documentation on the methods referenced here.

If you are placing your implementation in the ``dissect.target`` source tree, you'll need to register your implementation.
Do this by opening ``dissect/target/container.py`` and add your implementation to the bottom by using
:func:`~dissect.target.container.register`:

.. code-block:: python

    register("mycontainer", "MyContainer")
