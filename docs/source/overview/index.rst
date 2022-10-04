Overview
========

At `Fox-IT <https://fox-it.com>`_ and `NCC Group <https://nccgroup.com>`_, we are always looking to push our incident response
capabilities to the next level. Because no adversary, no matter how high-end, should be beyond our reach.
This led to the development of "dissect", a proprietary enterprise investigation framework that we have now open sourced
and shared with the world.

Dissect is the collective name of the many different projects that live in the ``dissect.*`` namespace. Many of these
projects are parsers or implementations for various file formats, such as ``dissect.ntfs`` for parsing NTFS
filesystems or ``dissect.hypervisor`` for parsing many virtual disk formats. However, when we're talking about
"dissect", we usually refer to one project in particular: ``dissect.target``.

``dissect.target`` is a host investigation framework made for enterprise forensics. It works on
:ref:`targets <overview/index:targets>`, which is basically any type of source data you may encounter in an
investigation. You don't have to worry anymore about how you're going to get something like a registry hive out of an
image, instead you're able to immediately get usable artefacts and investigation information out of any source data.
This allows you to spend more time on doing the fun and interesting work of an investigation, and less time on the
boring stuff, like extracting files and running a bunch of different tools on them.

Instead of focussing on a single system, ``dissect.target`` is designed to work on many targets at once.
A flexible architecture and plugin system allows our analysts to easily create new analysis capabilities that will
automatically work on all of the supported evidence formats.

Architecture
------------

Dissect is made up of many different libraries and multiple tools, which consume those libraries. An important decision in
the architecture of Dissect was to put libraries front and center, and develop tools on top of those libraries. Each library
has a single purpose and shouldn't "know too much". For example, an MBR/GPT/LVM2 implementation doesn't need to know how a
filesystem works, and an NTFS implementation doesn't need to know about partitions or Windows registry files.

By essentially dog feeding ourselves with these libraries, it ensures that each library has a usable API and doesn't get
cluttered. It also allows for incredible flexibility with how you put your code to use. We don't want to end up in a
situation where some functionality is only available in a CLI script. Everything is reusable and flexible.

However, you can't really do anything if you only have a bunch of libraries for parsing virtual disks and filesystems.
You'd end up in a situation where you're writing custom Python scripts for each investigation, not scalable at all.
This is exactly the situation we ended up in. We had all these fancy and fast parsers for various formats, but every
time you wanted to use it, you'd have to write or edit a script. This is where ``dissect.target`` comes into play.

In short, ``dissect.target`` is the glue between all these different libraries. It leverages all the different parsers
to deliver an easy to use and extendable investigation framework. In practise, this means that ``dissect.target`` allows
you to go straight from an ``.E01`` file to event logs in Splunk, without having to think about mounting, extracting or
parsing anything.

The way ``dissect.target`` goes about this is a layered approach. Each layer is interchangeable for a compatible layer,
and you can start from any layer. Let's go through each layer, taking an ``Example.vmx`` file as a practical example to
explain each layer.

Targets
~~~~~~~

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

Dissect also supports the concept of targets within targets, referred to as child targets. For example, when a
target contains a ``.vmdk`` file within itself, we can tell ``dissect.target`` to load that target from within the
context of the first target. This can be useful when dealing with hypervisors.

Say, for example, we opened a Hyper-V target locally from ``\\.\PhysicalDrive0``, we can parse the metadata
in ``ProgramData/Microsoft/Windows/Hyper-V/data.vmcx`` that tells us where all of the virtual machines are stored.
Then we can then use these paths and tell ``dissect.target`` to load another target from there. Reading all of these
files will still happen from ``\\.\PhysicalDrive0``, passing through the various abstraction layers of ``dissect.target``.
This allows Dissect to read the disks from running virtual machines, regardless of locks the operating has on these files.

On the technical side, everything eventually gets loaded into a ``Target`` Python object. This is not required
knowledge for working with Dissect, but may help when reading the documentation.

.. seealso::

    For more information about how the ``Target`` object works internally, or how targets within targets works, please
    refer to :doc:`/advanced/targets`.

Loaders
~~~~~~~

A loader in ``dissect.target`` is responsible for mapping any kind of source data into something the Dissect framework
understands. Loaders can be incredibly complex or incredibly simple, depending on what you are trying to achieve.

In our example of the ``Example.vmx`` file, we can parse the VMX file to retrieve the paths to all the VMDK files
associated with this VMX file. In this case, let's say that is ``Example-disk1.vmdk`` and ``Example-disk2.vmdk``, a
``C:`` and ``D:`` drive respectively.

.. seealso::

    For more information about how loaders work internally, please refer to :doc:`/advanced/loaders`.

Containers
~~~~~~~~~~

Containers in ``dissect.target`` can be seen as an abstraction layer for anything that looks like a raw disk.
It provides a unified API for all these different "containers", which basically boils down to it acting like
any other file-like object.

Continuing where our loader left off, we now have two ``.vmdk`` files we need to do something with. Since we have
a VMDK implementation in Dissect, we can tell the container layer to open each of these and add them as "disks".

.. seealso::

    For more information about how containers works internally, please refer to :doc:`/advanced/containers`.

Volumes
~~~~~~~

Volumes in ``dissect.target``, much like containers, are an abstraction layer for anything that looks like a raw volume.
Similar to containers, everything is a file-like object.

For each of our VMDKs, ``dissect.target`` will try to detect a volume system and return all found partitions.
For this example, let's say that each disk has just one partition, an NTFS volume.

For more information about how volumes and volume systems work internally, please refer to :doc:`/advanced/volumes`.

Filesystems
~~~~~~~~~~~

Filesystems is where it finally gets a little more exciting in ``dissect.target``. Again, they represent a filesystem
using a unified API. The API for this tries to mimic the Python standard library API as much as possible, to make working
with it as easy as possible for anyone with Python experience.

Anything that can be interpreted as a filesystem lives here. This, obviously, includes actual filesystems such as ``NTFS``
or ``ext4``, but also anything else that you can interpret as a filesystem. For example, a directory containing extracted
files (comparable to a ``chroot``), a tar file or a remote EDR agent API can all be interpreted as a filesystem in some way.

Continuing with our example, ``dissect.target`` will attempt to detect a filesystem on the two volumes we previously found.
It will succeed in detecting an ``NTFS`` filesystem on both volumes.

One important thing to know is that ``dissect.target`` relies heavily on virtual filesystems. These are fake filesystems
implementing the filesystem API, where we can map any file (real or virtual) to any path. This is used for e.g. creating
drive letters or mounting filesystems at specific paths.

.. seealso::

    For more information about how filesystems work internally, please refer to :doc:`/advanced/filesystems`.

Plugins
~~~~~~~

Automatically loading containers, volumes and filesystems can be considered the core functionality of ``dissect.target``.
In our example, we now have a target with two disks, two volumes and two filesystems, all done automatically. Nice, but still
not really that useful. We'd still have to write a ton of Python code ourselves to do anything useful with it. This is where
the plugin system of ``dissect.target`` comes into play.

Plugins is where we further refine a loaded target and what we can do with it. It's also the place where we can implement
actual functionality for e.g. extracting forensic artefacts. If you were to stack all of the previous layers in order, with
containers being at the bottom, plugins would be at the top. The idea is that you could swap any compatible component
within a layer with another, and it will all continue to work just fine.

In practise, this means that a plugin that's responsible for Windows event logs doesn't care where those event logs actually
come from. They can be from an NTFS filesystem (that can in turn be parsed from a VMDK), or they can come from a ``.tar`` file.

.. seealso::

    For more information about how plugins work internally, please refer to :doc:`/advanced/plugins`.

Operating systems
^^^^^^^^^^^^^^^^^

Plugins themselves are also layered. We start off with operating system plugins which are responsible for some OS specific
plumbing, such as:

* Further processing of operating systems that are normally loaded into memory (e.g. VyOS or ESXi)
* Mounting volumes to the correct drive letter/path
* Parsing OS specific information such as the version, IPs/network interfaces and users

Operating system plugins can themselves also be layered. For example, a Debian specific plugin can be layered on top of a
Linux plugin.

In our VMX example, we had two disks for the ``C:`` and ``D:`` drives respectively. The Windows plugin will parse the
registry to find out which drive needs to be mounted where, and makes sure the respective filesystems are available on the
correct drive letters.

Other plugins
^^^^^^^^^^^^^

Next we have auxiliary and "artefact" plugins. An example of an auxiliary plugin is the Windows registry plugin, which
provides an easy to use API for interacting with the Windows registry, which can then be used by all the other plugins.
An example of an artefact plugin is the Windows event log plugin, or the Windows services plugin, which leverages the
registry plugin!

Note that it's a deliberate design decision in Dissect that artefacts are only parsed from their intended/configured
locations. For example, when parsing Windows event logs we will only use the default and configured event log paths
(from the registry). Event logs in any other location on the filesystem will not be parsed.

Having specified the target from a VMX file, however, gives us the benefit that we know about both the ``C:`` and ``D:``
drives. If event logs are configured to be stored at ``D:\Logs``, there are no additional steps we need to take to
parse these. The event log plugin will read the configured log location and parse the logs found on the filesystem
associated with the ``D:`` drive.

Plugins can have four types of outputs: ``default``, ``yield``, ``record`` and ``none``. The output type of a plugin
can be seen when listing them by running ``target-query -l``.

* ``default``: Returns "basic types" such as strings, integers, lists
* ``yield``: Yields strings, useful for things like human readable timelines
* ``records``: A ``flow.record`` :ref:`record <overview/index:records>`
* ``none``: Returns nothing, useful for miscellaneous plugins that print things on their own (such as the plugin lister plugin!)

Records
-------

Records are a simple typed key/value storage format created by Fox-IT. You can think of it like JSON, but strongly
typed. For example, we may define a record as having a timestamp field of type ``datetime``, or an IP address field
of type ``net.ipaddress``. You can interact with specific attributes of these fields, too. For example, you can get the
``filename`` attribute of an ``uri`` field to just get the filename of that path.

Records are the primary output type when using the various functions of ``dissect.target``. On the command line,
this is mostly experienced through the :doc:`/tools/target-query` and :doc:`/tools/rdump` utilities.

Records and a range of utilities are implemented in :doc:`/projects/flow.record/index`.
