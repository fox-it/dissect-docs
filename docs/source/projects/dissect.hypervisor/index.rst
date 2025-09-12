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

Open QCOW2 snapshots
~~~~~~~~~~~~~~~~~~~~

For `qcow2` images there is support for backing-files and it can either be automatically loaded when opening a target.
The backing-file will automatically be read from the `qcow2` headers and dissect will attempt to load it.

.. code-block:: python
  target = Target.open(target_path)
  print(target.users())

Or, for more control, the path to the backing file can be passed when initializing a `qcow2` disk:

.. code-block:: python
  def open_qcow2_with_backing_file(snapshot_path: Path, backing_path: Path):
      # Open base QCOW2 image
      backing_fh = backing_path.open("rb")
      base_qcow2 = qcow2.QCow2(backing_fh)
      base_stream = base_qcow2.open()

      # Open snapshot QCOW2 image with base as backing file
      snapshot_fh = snapshot_path.open("rb")
      snapshot_qcow2 = qcow2.QCow2(
          snapshot_fh,
          backing_file=base_stream
      )
      snapshot_stream = snapshot_qcow2.open()

      return snapshot_stream, snapshot_fh, backing_fh, base_stream

  def analyze_image(snapshot_path: Path, backing_path: Path):
      # Open the QCOW2 snapshot along with its backing file and get file/stream handles
      snapshot_stream, snapshot_fh, backing_fh, base_stream = open_qcow2_with_backing_file(snapshot_path, backing_path)

      # Create a new Dissect target to analyze the disk image
      target = Target()
      # Add the snapshot stream to the target’s disks
      target.disks.add(snapshot_stream)
      # Resolve all disks, volumes and filesystems and load an operating system on the current
      target.apply()

      # Collect data from the snapshot
      print(target.users())

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
