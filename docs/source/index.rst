Dissect
=======

Welcome to the official documentation of Dissect!

Dissect is a collection of Python libraries and tools to facilitate enterprise-scale incident response and forensics.
It supports you, the analyst, from the moment of acquisition of artifacts, to normalisation and processing.

Dissect frees you from limitations by data formats and platforms and takes away concerns about how to access
investigation data. You can focus on performing analysis, developing complex analysis plugins or performing
research. You know, the cool stuff that we brag about on birthday parties. With Dissect, you can go from intake call
to patient zero in a matter of hours, even in infrastructures with thousands of systems.

With Dissect, beginner and intermediate analysts get direct access to a large collection of artefact parsers and
plugins that work quickly and easily on a large range of evidence formats. More advanced analysts with scripting
experience can also leverage Dissect`s full capabilities by creating new tools and plugins using the various Dissect
APIs and parsers.


.. note ::
    Read more about what Dissect is and how it works at :doc:`/overview/index` or check out what others
    have written about Dissect in :doc:`/resources/dissect-in-action`.


Getting Started
---------------

The easiest way to get started is to install the latest version of all Dissect projects from
`PyPI <https://pypi.python.org/pypi/dissect>`_:

.. code-block:: console

    $ pip install dissect

It is recommended that you use a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_.

.. note ::
    .. include:: /versions.rst

To quickly get familiar with Dissect, read on to :doc:`/usage/introduction`. If you're interested in what makes it
tick, continue reading at :doc:`/overview/index`.

Installing individual projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dissect is a collection of libraries and tools, so every Dissect project is individually installable. You'll find that
installing the ``dissect`` package from PyPI will install all available ``dissect.*`` packages for you! If, however,
you just want to work with the NTFS and registry parsers in your own scripts, you can opt to only install or depend
on those specific projects:

.. code-block:: console

    $ pip install dissect.ntfs dissect.regf

You can find an overview of all available Dissect projects and their documentation at :doc:`/projects/index`.

Using the Docker image
~~~~~~~~~~~~~~~~~~~~~~

If you simply want to get started with some of the examples without having to install anything, a basic Docker image
is available `here <https://github.com/orgs/fox-it/packages/container/package/dissect>`_ (`mirror <https://hub.docker.com/r/dissect/dissect>`_).
You can start using this image by executing the following command in your terminal:

.. code-block:: console

    $ docker run -it --rm -v /path/to/targets/:/mnt:ro ghcr.io/fox-it/dissect:3.2
    (<dissect version>) <container hash>:/workspace$

This will drop you in a shell environment with all the Dissect ``target-*`` :doc:`tools </tools/index>` at your disposal.
The purpose of the ``-v`` option is to mount a local directory inside the Docker container. You can use this to interact
with local data from within the Docker container.

Browser demo
~~~~~~~~~~~~

If you don't feel like doing the above, then there is an interactive browser demo available at
`try.dissect.tools <https://try.dissect.tools>`_ to play around with!

You can select evidence files from your local system, such as VMDK or EWF files, and explore some of the capabilities
of Dissect. Nothing gets uploaded to a server, it all happens locally thanks to `Pyodide <https://pyodide.org/en/stable/>`_!

.. caution::

    The browser demo was developed as a quick demo and is bound to be unstable. Not everything may work as expected.

Summary
-------

It's difficult to explain the full capabilities of Dissect in a few sentences, but it can best be summarized as
an attempt to bring "it just works" to the field of digital forensics. Analysts no longer need to concern themselves
with thinking about *how* they get artefacts from their source data and can instead focus on *what* artefacts
they want to analyse.

For example, with Dissect you can:

* Make a timeline of the event log from all investigation data at once;
* Identify anomalies in artefacts such as services, tasks and run keys over a large amount of investigation data;
* Perform incident response on partially ransomwared (encrypted) virtual machine disks;
* Perform complex IOC checks on thousands of hosts in a couple of hours;
* Export all USN journal records from a Bitlocker-encrypted disk to Splunk without waiting for decryption;
* Collect forensic artefacts from all live virtual machines directly from the hypervisor with no down time;
* Export all artefacts easily to any data format you want, for example CSV, JSON or Avro, or stream directly to Splunk or Elastic;
* ... and much more.

For more information about what Dissect is and how it works, read on at :doc:`/overview/index`.

.. toctree::
    :hidden:

    Home <self>
    /overview/index
    /projects/index
    /usage/index
    /tutorial/index
    /tools/index
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

.. toctree::
    :caption: Links
    :hidden:

    Try in your browser <https://try.dissect.tools/>
    GitHub <https://github.com/fox-it/dissect/>
    PyPI <https://pypi.org/project/dissect/>
