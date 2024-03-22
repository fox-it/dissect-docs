Children
========

Child targets are nested targets. Targets can contain nested targets, this is almost always the case if
the target is an hypervisor. After retrieving a child target, it behaves just like a regular target, all
the plugin methods are available. The following child targets are supported:

* VMware ESXi (also known as vSphere)
* VMWare Workstation
* Microsoft Hyper-V 
* Windows Subsystem for Linux (WSL2)
* Virtuozzo

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

To craft your own child plugin, subclass the ``ChildTargetPlugin`` and implement the
``list_children()`` method. Use the ``__type__`` attribute to specify the type of the child plugin (i.e. "wsl").


