Welcome to Dissect!
===================

Effortlessly extract and investigate **forensic artefacts** from any source with **Dissect**.
Go from intake call to patient zero in a matter of hours,
even in infrastructures with thousands of systems.


Quick Demo
----------

In just a couple of seconds you can query a **forensic image** or even open a shell!

.. image:: /images/demo.gif


Usage Example
-------------

One of the most prominent tools that Dissect offers is called *target-query*.
With this simple command you can, for example, extract all user accounts from a disk image: 

.. code-block:: console

    $ target-query pc.img -f users
    
    <windows/user ... name='systemprofile' ...>
    <windows/user ... name='LocalService' ...>
    <windows/user ... name='NetworkService' ...>
    <windows/user ... name='Mr. Evil' ...>
    
To see what other useful artefacts you can query use ``-l``:

.. code-block:: console

    $ target-query pc.img -l

This will list all Dissect functions and artefacts that are available for this image.
To list **all** functions and artefacts, regardless of the image, just leave out the image argument!

Try the :doc:`/tutorial` to get started!

Key features
------------

Dissect is a powerful artefact extractor and parser that saves you a lot of time.
With Dissect you can:

* Quickly **extract artefacts** from any source (for example IMG, EWF, Kape, DD, VDI, PVM).
* Access artefacts from almost any OS (for example Windows, macOS, Linux/Unix, ESXi).
* Access almost any filesystem (for example NTFS, EXT, XFS, QNX6).
* **Parse logs**, registry entries, cookies, history and more, directly from the source.
* Export findings to text, JSON, CSV or stream to datastores like Splunk, Elastic, MySQL.
* Feed, filter and script to process found data in any way you like.
* **Investigate images** with powerful tools like target-shell, target-mount or using our friendly Python API.

These features can enable you to:

* Make a timeline of the event log from all your investigation data at once.
* Identify anomalies in artefacts such as services, tasks and run keys over a large amount of investigation data.
* Do **incident response** on virtual machine disks encrypted by ransomware.
* **Extract artefacts** from LVM, RAID and other disk setups, without any manual configuration.
* Perform complex **IOC checks** on thousands of hosts in a couple of hours.
* Collect forensic artefacts from running virtual machines directly from the hypervisor without down time.


Learn more
----------

Excited? Great, so are we!
The next step is to get to know Dissect a little better.

* First, :doc:`/install` Dissect.
* Try the :doc:`/tutorial` to get started.
* Learn the basics of :doc:`/target-query`, :doc:`/target-shell`, :doc:`/target-mount`, :doc:`/acquire` and :doc:`/rdump`.
* Visit :doc:`/usage/introduction` for an in-depth introduction to Dissect.
* Visit :doc:`/tools/index` for an overview of each tool in the Dissect suite.

Or you can start by taking a look at some community articles and videos:
:doc:`/resources/dissect-in-action` or
:doc:`/resources/talks-and-conferences` to begin with.

Get in touch, join us on `github <https://github.com/fox-it/dissect.target>`_!


.. toctree::
    :hidden:
    
    Home <self>

.. toctree::
    :caption: Basics
    :hidden:

    Install </install>
    Tutorial </tutorial>
    Querying </target-query>
    Shell </target-shell>
    Mount </target-mount>
    Acquire </acquire>
    RDump </rdump>
    
    
.. toctree::
    :caption: In-Depth
    :hidden:
    
    /tools/index
    /projects/index
    /usage/index
    /plugins/index
    Architecture </overview/index>
    /advanced/index
    /api/index

.. toctree::
    :caption: Contributing
    :hidden:

    /contributing/developing
    /contributing/style-guide
    /contributing/tooling
    License </license>

.. toctree::
    :caption: Resources
    :hidden:

    /resources/dissect-in-action
    /resources/talks-and-conferences
    Try in your browser <https://try.dissect.tools/>
    GitHub <https://github.com/fox-it/dissect/>
    PyPI <https://pypi.org/project/dissect/>
