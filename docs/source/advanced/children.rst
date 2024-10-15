Children
========


Dissect also supports the concept of targets within targets, referred to as child targets. For example, when a
target contains a ``.vmdk`` file within itself, we can tell ``dissect.target`` to load that target from within the
context of the first target. This can be useful when dealing with hypervisors.

Say, for example, we opened a Hyper-V target locally from ``\\.\PhysicalDrive0``, we can parse the metadata
in ``ProgramData/Microsoft/Windows/Hyper-V/data.vmcx`` which tells us where all of the virtual machines are stored.
We can then use these paths and tell ``dissect.target`` to load another target from there. Reading all of these
files will still happen from ``\\.\PhysicalDrive0``, passing through the various abstraction layers of ``dissect.target``.
This allows Dissect to read the disks from running virtual machines, regardless of locks the operating has on these files.

Child targets can be anything that Dissect already supports, but we also provide some automatic detection of 
child targets for certain systems. Automatic child target detection is currently supported for:

* VMware ESXi (also known as vSphere)
* VMWare Workstation
* Microsoft Hyper-V 
* Windows Subsystem for Linux (WSL2)
* Virtuozzo

Using child targets
-------------------

To apply ``target-query`` to child targets simply add the ``--children`` flag like this:

.. code-block:: console

    $ target-query /path/to/target -f hostname --children

Replace the example path ``/path/to/target`` with the path to the host image.
To just query a specific child, simply use the ``--child`` option and provide the path to
the file within the host target that contains the child target:

.. code-block:: console

    $ target-query /path/to/target -f hostname --child /virtualmachines/host123.vmcx

Alternatively you can use the index number of the child:

.. code-block:: console

    $ target-query /path/to/target -f hostname --child 1

When using :doc:`target-shell </tools/target-shell>` you can access the child target by using the ``enter`` command
on the file that contains the child target:

.. code-block:: console

    $ enter host123.vmcx


Child target API
----------------


To obtain a list of nested targets use ``list_children``:

.. code-block:: python

    target = Target.open("host.img")
    target.list_children()

This will produce a list of records describing the child targets inside:

.. code-block:: console

    <target/child ... type='hyper-v' path='C:\Hyper-V\Virtual Machines\EC04F346-DB96-4700-AF5B-77B3C56C38BD.vmcx'>

You can now open each target by passing the path attribute to the ``target.open_child()`` method:

.. code-block:: python

    target.open_child(child.path)
    
To open all child targets of a target:

.. code-block:: python

    children = target.open_children()
    
This can also be done recursively by passing ``True`` as a parameter.
To open all child targets when opening a batch of targets:

.. code-block:: python

    all = Target.open_all(["hyper1.img","hyper2.img"], children=True)

Child targets are loaded through special ``Child plugins`` that reside in the
``/dissect/target/plugins/child`` folder. To get a list of all child plugins
available:

.. code-block:: python

    supported_children = child_plugins()

To craft your own child plugin, subclass the :class:`ChildTargetPlugin <dissect.target.plugin.ChildTargetPlugin>` and implement the
``list_children()`` method. Use the ``__type__`` attribute to specify the type of the child plugin (i.e. "wsl").

.. seealso::

    The :class:`HyperV <dissect.target.plugins.child.hyperv>` child plugin is a good example to get started!

