Targets
=======

One of the most important concepts of Dissect is that of a "target" as it is the input of
many Dissect tools.

In this section you will learn what targets are on a conceptual level and try out
a few tools that have targets as input.


What are targets?
-----------------

The basic definition of a target is as follows:

Target
  Data from a system that can be used to describe a state of that system, regardless of format.

In the context of this tutorial, 'data from a system' should be intepreted to mean filesystem data, which is usually the data under
investigation during forensics and incident response cases. However, more advanced types of targets do exist which are out of scope for now.


Examples of targets include but are not limited to:

* Physical hard disks: ``\\.\PHYSICALDRIVE#`` or ``/dev/sdX``
* Disk images: ``E01`` (Expert Witness Format) or ``RAW`` (dd)
* Virtual machine descriptors: ``vmx``, ``vmcx``, ``vbox``
* Virtual hard disks: ``vmdk`` or ``qcow2``
* Directory structure resembling the Windows or Unix filesystem hierarchy
* Tar archive(s) resembling a Windows or Unix filesystem hierarchy

.. seealso::

    For more technical information about targets, see :ref:`overview/index:targets`.

The beauty of targets in Dissect is that a target can be in a variety of formats (as seen in the list above),
but they all work transparently to the user!

Target examples
---------------

In the following examples, we will use the command ``target-query`` to get information about the operating system present in
a target. You will notice that we execute the command on three different representations of targets (RAW image, Virtual Machine
hard disk and your own disk) and we get the result without having to specify or convert the format!


FIXME OOK NOG IETS OVER NESTED TARGETS?


Running ``target-query`` on a RAW image:

.. code-block:: console

    $ target-query SCHARDT.001 -f os
    <Target SCHARDT.001> windows

Running ``target-query`` on a Virtual Machine Hard Disk image:

.. code-block:: console

    $ target-query IE11-Win81-VMWare-disk1.vmdk -f os
    <Target IE11-Win81-VMWare-disk1.vmdk> windows

Running ``target-query`` on your currently running system:

.. code-block:: console

    $ target-query / -f os
    <Target /> linux

As you can see in the examples above, we could use the *same* command on various inputs wihtout having to think about, or specify,
the format. We did not need to mount any filesystems or install additional software to handle ``vmdk`` files; all this information was
done natively by Dissect!

In other words, if during your investigations you come across a file (or set of files) that represent(s) a filesystem and you need to investigate,
and Dissect supports it, it can be used as a target in ``target-query`` or any of the other Dissect tools!

FIXME target-query -s of zodner? wanneer?

-s forceert string output
    vb runkeys zijn altijd records
    als je wilt greppen kost dat performance zodat je
    niet via rdump te hoeft

FIXME rdump -f (kleine lettr wel)

FIXME target-info voo CMDB use case

Takeaways
---------

The most important takeaways of this section are:

1. Most Dissect tools work on "targets"
2. Targets represent data of a system of investigation
3. Targets can come in multiple formats
4. Users need not think about the format of the targets; Dissect will handle conversion on-the-fly.
