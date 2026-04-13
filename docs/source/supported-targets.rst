Supported Targets
-----------------

Dissect supports a large range of formats.
From various disk images, volume systems, file systems and operating systems, to tarballs and proprietary backup formats, and everything combined!
This page aims to provide you with an overview of what you can expect Dissect to be able to handle!

Loaders
~~~~~~~

Loaders provide a way to interact with a "target" by combining and accessing source data into usable parts.
This creates a virtual representation of the original system.

.. seealso::

  For a deeper dive into how loaders work, see :doc:`loaders </advanced/loaders>`.

In most cases, Dissect selects the appropriate loader automatically based on the file you target.
It does this by looking at things like the file type, folder structure or special configurations files.
If needed, you can choose the loader yourself by using ``-L <loader type>`` option or by using the URI-style notation ``<loader type>://``.

.. code-block:: console

  target-query -f func /path/to/target.ab
  target-query -f func -L ab /path/to/target
  target-query -f func ab:///path/to/target

.. important::

  Just because it does not have a loader, does not mean Dissect cannot open it! In those cases, Dissect falls back to a "raw loader",
  which allows it to be opened as any of the :ref:`supported containers <supported-targets:Containers>` or even
  :ref:`supported filesystems <supported-targets:Filesystems>`. Whether a target is supported
  as a loader, a container or a filesystem depends on implementation details for that specific format.

.. dissect-supported-table:: Supported loaders
  :header-rows: 1
  :widths: 20 15 5
  :source-path: dissect.target/dissect/target/loaders
  :blacklist: cyber,phobos,itunes,target,vb,asdf,log,vmsupport,res,direct,profile,pvs

  * - Description
    - Format
    - API
  * - Android backup
    - ``.ab``
    - :mod:`ab <dissect.target.loaders.ab>`
  * - Acquire
    - ZIP or tar with Acquire structure
    - :mod:`acquire <dissect.target.loaders.acquire>`
  * - AccessData AD1
    - ``.ad1``
    - :mod:`ad1 <dissect.target.loaders.ad1>`
  * - Carbon Black Live Response endpoint
    - ``cb://`` or ``-L cb`` [#f1]_
    - :mod:`cb <dissect.target.loaders.cb>`
  * - Cellebrite UFED export
    - ``.ufdx``, ``.ufd``
    - :mod:`cellebrite <dissect.target.loaders.cellebrite>`
  * - Docker and OCI container images
    - tar file with Docker or OCI image structure
    - :mod:`containerimage <dissect.target.loaders.containerimage>`
  * - Local directory
    - Common OS structure (``path/Windows/System32`` or ``path/etc``)
    - :mod:`dir <dissect.target.loaders.dir>`
  * - Microsoft Hyper-V virtual machine configuration
    - ``.vmcx``, ``.xml``
    - :mod:`hyperv <dissect.target.loaders.hyperv>`
  * - iTunes backup
    - Directory with iTunes backup structure
    - :mod:`itunes <dissect.target.loaders.itunes>`
  * - KAPE
    - Directory or ``.vhdx`` with KAPE structure
    - :mod:`kape <dissect.target.loaders.kape>`
  * - Libvirt XML configuration
    - ``.xml``
    - :mod:`libvirt <dissect.target.loaders.libvirt>`
  * - Local system (automatically load all drives such as ``/dev/sda`` or ``\\.\PhysicalDrive0``)
    - ``local``
    - :mod:`local <dissect.target.loaders.local>`
  * - MQTT broker
    - ``mqtt://`` or ``-L mqtt`` [#f2]_
    - :mod:`mqtt <dissect.target.loaders.mqtt>`
  * - Netscaler Techsupport Collector
    - tar with Netscaler Techsupport structure
    - :mod:`nscollector <dissect.target.loaders.nscollector>`
  * - Open Virtual Appliance (OVA)
    - ``.ova``
    - :mod:`ova <dissect.target.loaders.ova>`
  * - Podman OCI overlay
    - Directory with Podman overlay structure
    - :mod:`overlay <dissect.target.loaders.overlay>`
  * - Docker overlay2
    - Directory with Docker overlay2 structure
    - :mod:`overlay2 <dissect.target.loaders.overlay2>`
  * - Open Virtualization Format (OVF)
    - ``.ovf``
    - :mod:`ovf <dissect.target.loaders.ovf>`
  * - Proxmox virtual machine configuration
    - ``.conf``
    - :mod:`proxmox <dissect.target.loaders.proxmox>`
  * - Parallels virtual machine directory
    - ``.pvm``,
    - :mod:`pvm <dissect.target.loaders.pvm>`
  * - Parallels virtual machine configuration
    - ``config.pvs``
    - :mod:`pvs <dissect.target.loaders.pvs>`
  * - Single raw binary file
    - Default fallback for unknown files
    - :mod:`raw <dissect.target.loaders.raw>`
  * - Multiple raw binary files
    - Paths with ``+`` (``/dev/vda+/dev/vdb``)
    - :mod:`multiraw <dissect.target.loaders.multiraw>`
  * - Remote Dissect agent
    - ``remote://`` or ``-L remote``
    - :mod:`remote <dissect.target.loaders.remote>`
  * - Remote SMB server
    - ``smb://`` or ``-L smb`` [#f3]_
    - :mod:`smb <dissect.target.loaders.smb>`
  * - Tanium
    - Directory with Tanium structure
    - :mod:`tanium <dissect.target.loaders.tanium>`
  * - (Compressed) tar
    - ``.tar``, ``.tar.<comp>``, ``.t<comp>``
    - :mod:`tar <dissect.target.loaders.tar>`
  * - Unix-like Artifacts Collector (UAC)
    - Directory, ZIP or tar with UAC structure
    - :mod:`uac <dissect.target.loaders.uac>`
  * - UTM virtual machine
    - ``.utm``
    - :mod:`utm <dissect.target.loaders.utm>`
  * - Oracle VirtualBox virtual machine
    - ``.vbox``
    - :mod:`vbox <dissect.target.loaders.vbox>`
  * - Veeam Backup (VBK)
    - ``.vbk``
    - :mod:`vbk <dissect.target.loaders.vbk>`
  * - Rapid7 Velociraptor
    - Directory or ZIP with Velociraptor structure
    - :mod:`velociraptor <dissect.target.loaders.velociraptor>`
  * - Proxmox Virtual Machine Archive (VMA)
    - ``.vma``
    - :mod:`vma <dissect.target.loaders.vma>`
  * - VMware Fusion virtual machine
    - ``.vmwarevm``
    - :mod:`vmwarevm <dissect.target.loaders.vmwarevm>`
  * - VMware virtual machine configuration
    - ``.vmx``
    - :mod:`vmx <dissect.target.loaders.vmx>`
  * - Citrix Hypervisor backup (XVA)
    - ``.xva``
    - :mod:`xva <dissect.target.loaders.xva>`
  * - ZIP
    - ``.zip``
    - :mod:`zip <dissect.target.loaders.zip>`

.. [#f1] Requires ``dissect.target[cb]``
.. [#f2] Requires ``dissect.target[mqtt]``
.. [#f3] Requires ``dissect.target[smb]``

Containers
~~~~~~~~~~

Containers let Dissect interact with a disk-like structure in a consistent way.
These can be virtual machine files, forensic containers or a hard disk itself.

.. seealso::

  For a deeper understanding on how containers work, see :doc:`containers <advanced/containers>`.

Dissect can select the appropriate container automatically based on either the file extension or file magic.
For example, the QCOW2 container gets selected if the file extension is ``.qcow2`` or if the first bytes of the file are ``b"QFI\xfb"``.

.. dissect-supported-table:: Supported containers
  :header-rows: 1
  :widths: 15 5 5
  :source-path: dissect.target/dissect/target/containers
  :blacklist: raw,asdf,hds,split

  * - Description
    - Format
    - API
  * - Apple Sparse Image Format
    - ``.asif``
    - :mod:`asif <dissect.target.containers.asif>`
  * - FTK Expert Witness Disk Image Format (EWF)
    - ``.E01``, ``.L01``
    - :mod:`ewf <dissect.target.containers.ewf>`
  * - Fortinet firmware
    - ``*-fortinet.out``
    - :mod:`fortifw <dissect.target.containers.fortifw>`
  * - Parallels HDD virtual disk
    - ``.hdd``
    - :mod:`hdd <dissect.target.containers.hdd>`
  * - Parallels HDS sparse virtual disk
    - ``.hds``
    - :mod:`hds <dissect.target.containers.hds>`
  * - QEMU QCOW2
    - ``.qcow2``
    - :mod:`qcow2 <dissect.target.containers.qcow2>`
  * - VirtualBox VDI virtual disk
    - ``.vdi``
    - :mod:`vdi <dissect.target.containers.vdi>`
  * - Hyper-V VHD virtual disk
    - ``.vhd``
    - :mod:`vhd <dissect.target.containers.vhd>`
  * - Hyper-V VHDX virtual disk
    - ``.vhdx``
    - :mod:`vhdx <dissect.target.containers.vhdx>`
  * - VMware virtual disk
    - ``.vmdk``
    - :mod:`vmdk <dissect.target.containers.vmdk>`

Partition Schemes and Volume Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dissect supports most common partition schemes. Nested partitions are supported as well.

.. dissect-supported-table:: Supported Partition Schemes
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.volume/dissect/volume/disk/schemes

  * - Description
    - API
  * - Apple Partition Map (APM)
    - :mod:`apm <dissect.volume.disk.schemes.apm>`
  * - BSD Disklabel
    - :mod:`bsd <dissect.volume.disk.schemes.bsd>`
  * - GUID Partition Table (GPT)
    - :mod:`gpt <dissect.volume.disk.schemes.gpt>`
  * - Master Boot Record (MBR)
    - :mod:`mbr <dissect.volume.disk.schemes.mbr>`

Besides these standard partition schemes, Dissect supports disks in RAID configurations or disks with logical volumes that span multiple disks.

.. seealso::

  For more details, see :doc:`volumes <advanced/volumes>`.

.. dissect-supported-table:: Supported volume systems
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.target/dissect/target/volumes
  :blacklist: disk,luks,bde

  * - Description
    - API
  * - DDF (Disk Data Format) RAID, common in Dell RAID controllers
    - :mod:`ddf <dissect.target.volumes.ddf>`
  * - LVM2
    - :mod:`lvm2 <dissect.target.volumes.lvm>`
  * - Linux MD RAID
    - :mod:`md <dissect.target.volumes.md>`
  * - VMFS LVM
    - :mod:`vmfs <dissect.target.volumes.vmfs>`

Dissect also has decryption capability for some well known systems.
This functionality can be accessed with a keychain file (specified with ``-K``) with multiple passphrases or a keychain value (``-Kv``) in most Dissect tools.

.. dissect-supported-table:: Supported encrypted volume systems
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.target/dissect/target/volumes
  :blacklist: disk,ddf,lvm,md,vmfs

  * - Description
    - API
  * - LUKS (version 1 and 2)
    - :mod:`luks <dissect.target.volumes.luks>`
  * - BitLocker (all configurations and versions, including EOW)
    - :mod:`bde <dissect.target.volumes.bde>`

Filesystems
~~~~~~~~~~~

In Dissect, filesystems go beyond traditional disk-based structures.
If it behaves like a filesystem, Dissect can likely treat it as one.
This includes both standard filesystems and formats that resemble filesystem behavior.

There might be some overlap with loaders and containers, as some formats can function in multiple roles,
or need implementation in different areas to work correctly.

.. seealso::

  For more details, see :doc:`Filesystems </advanced/filesystems>`.

.. dissect-supported-table:: Supported filesystems
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.target/dissect/target/filesystems
  :blacklist: zip,smb,itunes,cb,overlay,ntds,tar,dir

  * - Description
    - API
  * - AccessData AD1
    - :mod:`ad1 <dissect.target.filesystems.ad1>`
  * - Apple File System (APFS)
    - :mod:`apfs <dissect.target.filesystems.apfs>`
  * - Linux Btrfs
    - :mod:`btrfs <dissect.target.filesystems.btrfs>`
  * - CPIO archive
    - :mod:`cpio <dissect.target.filesystems.cpio>`
  * - Linux cramfs
    - :mod:`cramfs <dissect.target.filesystems.cramfs>`
  * - exFAT
    - :mod:`exfat <dissect.target.filesystems.exfat>`
  * - Linux EXT2, EXT3, EXT4
    - :mod:`extfs <dissect.target.filesystems.extfs>`
  * - FAT12, FAT16, FAT32
    - :mod:`fat <dissect.target.filesystems.fat>`
  * - BSD Fast Filesystem (FFS)
    - :mod:`ffs <dissect.target.filesystems.ffs>`
  * - Linux Journaling Flash Filesystem (JFFS)
    - :mod:`jffs <dissect.target.filesystems.jffs>`
  * - Network File Share (NFS)
    - :mod:`nfs <dissect.target.filesystems.nfs>`
  * - Microsoft NTFS
    - :mod:`ntfs <dissect.target.filesystems.ntfs>`
  * - QNX4 and QNX6
    - :mod:`qnxfs <dissect.target.filesystems.qnxfs>`
  * - Linux SquashFS
    - :mod:`squashfs <dissect.target.filesystems.squashfs>`
  * - Veeam Backup (VBK)
    - :mod:`vbk <dissect.target.filesystems.vbk>`
  * - VMware (VMFS)
    - :mod:`vmfs <dissect.target.filesystems.vmfs>`
  * - VMware vmtar
    - :mod:`vmtar <dissect.target.filesystems.vmtar>`
  * - Linux XFS
    - :mod:`xfs <dissect.target.filesystems.xfs>`

Operating Systems
~~~~~~~~~~~~~~~~~

Dissect tries to automatically figure out what operating system is available on the target, based on known file locations and structures.
Once the operating system is known, it enables you to get more accurate information from the system, for example, the user or network configuration.

.. dissect-supported-table:: Supported operating systems
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.target/dissect/target/plugins
  :glob-pattern: "**/_os.py"
  :blacklist: default

  * - Description
    - API
  * - Windows
    - :mod:`windows <dissect.target.plugins.os.windows._os>`
  * - Generic Unix
    - :mod:`unix <dissect.target.plugins.os.unix._os>`
  * - BSD
    - :mod:`unix.bsd <dissect.target.plugins.os.unix.bsd._os>`
  * - Citrix
    - :mod:`unix.bsd.citrix <dissect.target.plugins.os.unix.bsd.citrix._os>`
  * - FreeBSD
    - :mod:`unix.bsd.freebsd <dissect.target.plugins.os.unix.bsd.freebsd._os>`
  * - OpenBSD
    - :mod:`unix.bsd.openbsd <dissect.target.plugins.os.unix.bsd.openbsd._os>`
  * - Generic Darwin
    - :mod:`unix.bsd.darwin <dissect.target.plugins.os.unix.bsd.darwin._os>`
  * - iOS
    - :mod:`unix.bsd.darwin.ios <dissect.target.plugins.os.unix.bsd.darwin.ios._os>`
  * - macOS
    - :mod:`unix.bsd.darwin.macos <dissect.target.plugins.os.unix.bsd.darwin.macos._os>`
  * - ESXi
    - :mod:`unix.esxi <dissect.target.plugins.os.unix.esxi._os>`
  * - Generic Linux
    - :mod:`unix.linux <dissect.target.plugins.os.unix.linux._os>`
  * - Android
    - :mod:`unix.linux.android <dissect.target.plugins.os.unix.linux.android._os>`
  * - FortiOS
    - :mod:`unix.linux.fortios <dissect.target.plugins.os.unix.linux.fortios._os>`
  * - OpenSUSE
    - :mod:`unix.linux.suse <dissect.target.plugins.os.unix.linux.suse._os>`
  * - RedHat
    - :mod:`unix.linux.redhat <dissect.target.plugins.os.unix.linux.redhat._os>`
  * - Debian
    - :mod:`unix.linux.debian <dissect.target.plugins.os.unix.linux.debian._os>`
  * - Proxmox
    - :mod:`unix.linux.debian.proxmox <dissect.target.plugins.os.unix.linux.debian.proxmox._os>`
  * - VyOS
    - :mod:`unix.linux.debian.vyos <dissect.target.plugins.os.unix.linux.debian.vyos._os>`

Child Targets
~~~~~~~~~~~~~

Dissect supports identifying, listing and querying *child targets*.
These are targets within other targets, such as virtual machines or containers.
Dissect finds these by looking inside configuration files on a target.
It can do this recursively, and look for *child targets* inside the *child targets* for even more *child targets*.

.. seealso::

  For more details, see :ref:`Child targets <advanced/targets:Targets in targets>`.

.. dissect-supported-table:: Supported child targets
  :header-rows: 1
  :widths: 20 5
  :source-path: dissect.target/dissect/target/plugins/child

  * - Description
    - API
  * - Colima containers
    - :mod:`colima <dissect.target.plugins.child.colima>`
  * - Docker containers
    - :mod:`docker <dissect.target.plugins.child.docker>`
  * - ESXi virtual machines
    - :mod:`esxi <dissect.target.plugins.child.esxi>`
  * - Hyper-V virtual machines
    - :mod:`hyperv <dissect.target.plugins.child.hyperv>`
  * - Lima containers and virtual machines
    - :mod:`lima <dissect.target.plugins.child.lima>`
  * - Parallels virtual machines
    - :mod:`parallels <dissect.target.plugins.child.parallels>`
  * - Podman containers
    - :mod:`podman <dissect.target.plugins.child.podman>`
  * - Proxmox virtual machines
    - :mod:`proxmox <dissect.target.plugins.child.proxmox>`
  * - QEMU virtual machines
    - :mod:`qemu <dissect.target.plugins.child.qemu>`
  * - Oracle VirtualBox virtual machines
    - :mod:`virtualbox <dissect.target.plugins.child.virtualbox>`
  * - Virtuozzo containers
    - :mod:`virtuozzo <dissect.target.plugins.child.virtuozzo>`
  * - VMware Workstation virtual machines
    - :mod:`vmware_workstation <dissect.target.plugins.child.vmware_workstation>`
  * - Windows Subsystem for Linux 2 (WSL2) instances
    - :mod:`wsl <dissect.target.plugins.child.wsl>`
