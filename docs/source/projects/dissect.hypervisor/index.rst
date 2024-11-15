dissect.hypervisor
==================

.. button-link:: https://github.com/fox-it/dissect.hypervisor
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for various hypervisor disk and configuration files.

* Metadata descriptors

  * Hyper-V VMCX and friends (:class:`~dissect.hypervisor.descriptor.hyperv.HyperVFile`)
  * OVF (:class:`~dissect.hypervisor.descriptor.ovf.OVF`)
  * VMX (:class:`~dissect.hypervisor.descriptor.vmx.VMX`)

* Virtual disks

  * QCOW2 (:class:`~dissect.hypervisor.descriptor.qcow2.QCow2`)
  * VDI (:class:`~dissect.hypervisor.descriptor.vdi.VDI`)
  * VHD (:class:`~dissect.hypervisor.descriptor.vhd.VHD`)
  * VHDX (:class:`~dissect.hypervisor.descriptor.vhdx.VHDX`)
  * VMDK (:class:`~dissect.hypervisor.descriptor.vmdk.VMDK`)

* Miscellaneous

  * ESXi envelope (:class:`~dissect.hypervisor.util.envelope.Envelope`) and key store
    (:class:`~dissect.hypervisor.util.envelope.KeyStore`)
  * ESXi visortar/vmtar (:mod:`~dissect.hypervisor.util.vmtar`)

Installation
------------

``dissect.hypervisor`` is available on `PyPI <https://pypi.org/project/dissect.hypervisor/>`_.

.. code-block:: console

    $ pip install dissect.hypervisor

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with a few CLI tools, so you primarily interact with it from Python. For example, to open
a VMDK for reading:

.. code-block:: python

    from dissect.hypervisor.vmdk import VMDK

    with open("/path/to/file.vmdk", "rb") as fh:
        disk = VMDK(fh)
        print(disk.read(512))

Many of the parsers in this package behave in a very similar way, so check the API reference to see how to utilize the
parser you need.

Tools
-----

.. sphinx_argparse_cli::
    :module: dissect.hypervisor.tools.envelope
    :func: main
    :prog: envelope-decrypt
    :description: Utility to decrypt ESXi envelope files with a given keystore file.
    :hook:

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.hypervisor`.
