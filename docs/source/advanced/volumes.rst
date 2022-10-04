Volumes
=======

Volume systems can be deceivingly complex. Basic volume systems such as MBR and GPT are easy enough, but things
quickly scale in complexity once you start considering logical volume managers such as
`LVM2 <https://sourceware.org/lvm2/>`_, or full volume encryption techniques such as
`LUKS <https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup>`_ or
`Bitlocker <https://docs.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-overview>`_.
While there are some tools available to work with some of these solutions, they often involve a lot of manual steps
and are tricky to automate. This makes scaling difficult once you need to analyse, for example, over a thousand
virtual machines with varying LVM2 configurations.

The volume system abstraction layer in ``dissect.target`` makes working with these different volume systems a lot
easier. There are implementations available for most commonly used volume systems, which will automatically be
discovered and used when using the various :doc:`tools </tools/index>` in ``dissect.target``. You can also choose
to manually leverage these implementations by using the API in :mod:`dissect.target.volume`, or choose to go one level
deeper and directly use the API from the individual Dissect libraries, such as :doc:`/projects/dissect.volume/index`.

.. seealso::

    To see how to open a volume system in Python, continue reading :ref:`here <advanced/api:volumes>`.

    View all available volume implementations at :mod:`dissect.target.volumes`.

Writing your own
----------------

Writing your own volume system is a little more complicated in comparison to loaders, containers, filesystems or plugins.
This is because of the way how different types of volume systems are currently integrated into ``dissect.target``.
Right now, the volume system layer works a little something like this:

* A MBR/GPT/APM volume system is opened and all discovered volumes are added, if any.
* All discovered volumes are checked to see if they are part of a logical volume system.

  * If any are, each discovered logical volume system is opened and all discovered logical volumes are added, if any.

* All discovered volumes are checked to see if they are part of an encrypted volume system.

  * If any are, each encrypted volume system is opened and all transparently decrypted volumes are added, if any.

When loading your own modules, as described in :ref:`advanced/api:loading your own modules`, you could append your own
logical or encrypted volume system to :data:`~dissect.target.volume.LOGICAL_VOLUME_MANAGERS` or
:data:`~dissect.target.volume.ENCRYPTED_VOLUME_MANAGERS`, respectively. Although this will currently work, this is bound
to change in the future so it shouldn't be relied on. The basic volume system is currently hardcoded to be MBR/GPT/APM.

If you still wish to write your own volume system, your best method will be to add a new implementation in the
``dissect.target`` source tree at ``dissect/target/volumes``. This method requires you to have a source checkout and working
development setup of ``dissect.target``.

.. seealso::

    Interested in developing for Dissect? Read more at :doc:`/contributing/developing`.

There are three types of volume systems you can implement:

* :class:`~dissect.target.volume.VolumeSystem`
* :class:`~dissect.target.volume.LogicalVolumeSystem`
* :class:`~dissect.target.volume.EncryptedVolumeSystem`

Each has specific methods that you are required to implement. It's recommended you read their documentation and use the
existing implementations as reference. You can use the boilerplate below to get started with a basic volume system:

.. code-block:: python

    from typing import BinaryIO, Iterator, Union

    from dissect.target.volume import Volume, VolumeSystem


    class MyVolumeSystem(VolumeSystem):
        def __init__(self, fh: Union[BinaryIO, list[BinaryIO]], *args, **kwargs):
            # Do your initialization here, for example, initialize a parser:
            # self._myparser = MyParser(fh)
            # Call ``super().__init__`` with the original file-like object(s) and serial if available
            super().__init__(fh, serial=None, *args, **kwargs)

        @staticmethod
        def detect(fh: BinaryIO) -> bool:
            # Perform detection for your volume system from a binary file-like object here
            # For example, check a specific magic value
            raise NotImplementedError()

        def _volumes(self) -> Iterator[Volume]:
            # Yield all ``Volume`` objects here, and fill in all necessary or available attributes:
            # Refer to the documentation of the ``Volume`` class for more details.
            raise NotImplementedError()

.. seealso::

    You can refer to the API documentation of the :class:`~dissect.target.volume.VolumeSystem` and
    :class:`~dissect.target.volume.Volume` class for more documentation on the methods referenced here.
    You can also reference :class:`~dissect.target.volume.LogicalVolumeSystem` or
    :class:`~dissect.target.volume.EncryptedVolumeSystem` for more information on writing your own logical or encrypted
    volume system respectively.
