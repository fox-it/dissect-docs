Supported targets
-----------------

Dissect supports a large range of formats. From various disk images, volume systems, file systems and operating systems, to tarballs and proprietary backup formats, and everything combined! This page aims to provide you with an overview of what you can expect Dissect to be able to handle!

Loaders
~~~~~~~

Loaders provide a way to interact with a "target" by combining and accessing source data into usable components for ``dissect.target``.
The goal is to build a virtual representation of the original system.

.. seealso::

   For a deeper dive into how loaders work, see :doc:`loaders </advanced/loaders>`.

In most cases, Dissect selects the appropriate loader automatically based on the file you target.
This can be based on the file extension, a specific directory structure inside the file (e.g. inside a zip file) or a specific configuration inside the file.
However, there is an option to select a loader manually using ``-L <loader type>`` flag or with URI-style notation ``<loader type>://``.

.. code-block:: bash

   target-query -f func -L ab /path/to/target
   target-query -f func ab:///path/to/target
   target-query -f func /path/to/target.ab

.. list-table:: Supported Loaders
   :header-rows: 1
   :widths: 15 20 10 5

   * - Name
     - Description
     - Extension
     - Type
   * - Android Backup
     - Android backup files.
     - ``.ab``
     - :class:`ab <dissect.target.loaders.ab.AndroidBackupLoader>`
   * - Carbon Black
     - Carbon Black Live Response endpoints. Can only be used directly with ``cb://`` or ``-L cb``.
     -
     - :class:`cb <dissect.target.loaders.cb.CbLoader>`
   * - Cellebrite
     - Cellebrite UFED exports files.
     - ``.ufdx``, ``.ufd``
     - :class:`cellebrite <dissect.target.loaders.cellebrite.CellebriteLoader>`
   * - Directory
     - Use a local directory as the root of a virtual filesystem.
     -
     - :class:`dir <dissect.target.loaders.dir.DirLoader>`
   * - Hyper-V
     - Microsoft Hyper-V configuration files.
     - ``.vmcx``, ``.xml``
     - :class:`hyperv <dissect.target.loaders.hyperv.HyperVLoader>`
   * - Itunes Backup
     - iTunes backup files. Only from a directory that contains a ``Manifest.plist`` file.
     -
     - :class:`itunes <dissect.target.loaders.itunes.ITunesLoader>`
   * - Kape
     - KAPE forensic image format files. Only if the file or directory contains Kape specific directories.
     - ``.vhdx`` or ``directory/``
     - :class:`kape <dissect.target.loaders.kape.KapeLoader>`
   * - Libvirt
     - Libvirt xml configuration files.
     - ``.xml``
     - :class:`libvirt <dissect.target.loaders.libvirt.LibvirtLoader>`
   * - Local
     - Interpret the local system inside Dissect.
     -
     - :class:`local <dissect.target.loaders.local.LocalLoader>`
   * - Log
     - Target specific log files. Can only be used directly with ``cb://`` or ``-L log``.
     -
     - :class:`log <dissect.target.loaders.log.LogLoader>`
   * - MQTT
     - MQTT broker. Can only be used directly with ``mqtt://`` or ``-L mqtt``.
     -
     - :class:`mqtt <dissect.target.loaders.mqtt.MqttLoader>`
   * - OVA
     - Virtual Appliance files.
     - ``.ova``
     - :class:`ova <dissect.target.loaders.ova.OvaLoader>`
   * - Overlay
     - Construct a filesystem of the different layers of a ``podman`` container directory.
     -
     - :class:`overlay <dissect.target.loaders.overlay.OverlayLoader>`,
   * - Overlay2
     - Construct a filesystem of the different layers of a ``docker`` container directory.
     -
     - :class:`overlay2 <dissect.target.loaders.overlay2.Overlay2Loader>`
   * - Open Virtualization Format
     - Open Virtualization Format (OVF) files.
     - ``.ovf``
     - :class:`ovf <dissect.target.loaders.ovf.OvfLoader>`
   * - Phobos
     - Phobos Ransomware files.
     - ``.eight``
     - :class:`phobos <dissect.target.loaders.phobos.PhobosLoader>`
   * - Proxmox
     - Proxmox VM configuration files.
     - ``.conf``
     - :class:`proxmox <dissect.target.loaders.proxmox.ProxmoxLoader>`
   * - Parallels VM
     - Parallels VM directory (.pvm) and the conviguration file (config.pvs)
     - ``.pvm``, ``config.pvs``
     - :class:`pvm <dissect.target.loaders.pvm.PvmLoader>`,
       :class:`pvs <dissect.target.loaders.pvs.PvsLoader>`
   * - Raw
     - Raw binary files such as disk images.
       To load multiple raw containers in a single target, use ``MultiRaw``.
       To use this loader automatically use ``+`` to chain disks. E.g. ``/dev/vda+/dev/vdb`` 
     - 
     - :class:`raw <dissect.target.loaders.raw.RawLoader>`,
       :class:`multiraw <dissect.target.loaders.multiraw.MultiRawLoader>`
   * - Remote
     - Connect to a remote target that runs a compatible Dissect agent. Can only be used directly with ``remote://`` or ``-L remote``.
     -
     - :class:`remote <dissect.target.loaders.remote.RemoteLoader>`
   * - SMB
     - Use an SMB connection to user remote SMB servers as a target.
       This particular loader requires ``impacket`` to be installed.
       Can only be used directly with ``smb://`` or ``-L smb``.
     -
     - :class:`smb <dissect.target.loaders.smb.SmbLoader>`
   * - Tanium
     - Tanium forensic image format files.
     -
     - :class:`tanium <dissect.target.loaders.tanium.TaniumLoader>`
   * - Tar
     - (Compressed) Tar files, docker container images and output files from Acquire or UAC.
     - ``.tar``, ``.tar.<comp>``, ``.t<comp>``
     - :class:`tar <dissect.target.loaders.tar.TarLoader>`
   * - Target
     - Load target system using a target file.
     - ``.target``
     - :class:`target <dissect.target.loaders.target.TargetLoader>`
   * - Unix-like Artifacts Collector
     - UAC tool output. Detects whether the directory contains ``uac.log`` and a ``[root]`` directory.
     -
     - :class:`uac <dissect.target.loaders.uac.UacLoader>`
   * - UTM
     - UTM virtual machine files.
     - ``*.utm/`` directory.
     - :class:`utm <dissect.target.loaders.utm.UtmLoader>`
   * - VB
     - .. TODO: looks like it supports rawcopy or something.
     -
     - :class:`vb <dissect.target.loaders.vb.VBLoader>`
   * - Virtual Box
     - Oracle VirtualBox files.
     - ``.vbox``
     - :class:`vbox <dissect.target.loaders.vbox.VBoxLoader>`
   * - Veaam Backup
     - Load Veaam Backup (VBK) files.
     - ``.vbk``
     - :class:`vbk <dissect.target.loaders.vbk.VbkLoader>`
   * - Velociraptor
     - Rapid7 Velociraptor forensic image files. Either loads in the zip file or a directory containing the contents.
     -
     - :class:`velociraptor <dissect.target.loaders.velociraptor.VelociraptorLoader>`
   * - Virtual Machine Archive
     - Proxmox Virtual Machine Archive files.
     - ``.vma``
     - :class:`vma <dissect.target.loaders.vma.VmaLoader>`
   * - VMware Fusion
     - VMware Fusion virtual machines.
     - ``.vmwarevm``
     - :class:`vmwarevm <dissect.target.loaders.vmwarevm.VmwarevmLoader>`
   * - VMware VM configuration
     - VMware virtual machine configuration files.
     - ``.vmx``
     - :class:`vmx <dissect.target.loaders.vmx.VmxLoader>`
   * - XVA
     - Citrix Hypervisor format files.
     - ``.xva``
     - :class:`xva <dissect.target.loaders.xva.XvaLoader>`
   * - Zip
     - Zip files themselves or load the output of tools like Acquire or UAC.
     - ``.zip``
     - :class:`zip <dissect.target.loaders.zip.ZipLoader>`

Containers
~~~~~~~~~~

Containers are the abstraction layer for anything that looks (or should look) like a raw disk.
They allow Dissect to interpret and interact with disk-like data structures in a consistent way.

.. seealso::

   For a deeper understanding on how containers work, see :doc:`containers <advanced/containers>`.

The table below lists the supported container formats.

.. list-table:: Supported Containers
   :header-rows: 1
   :widths: 20 5 20 5

   * - Container
     - Extension
     - Description
     - API
   * - Apple Sparse Image Format
     - ``.asif``
     - No Documentation
     - :class:`here <dissect.target.containers.asif.AsifContainer>`
   * - Expert Witness Disk Image Format
     - ``.E01``, ``.L01``, ``.Ex01``, ``.Lx01`` 
     - FTK Expert witness data format.
     - :class:`here <dissect.target.containers.ewf.EwfContainer>`
   * - Fortinet Firmware
     - ``*-fortinet.out``
     - No documentation
     - :class:`here <dissect.target.containers.fortifw.FortiFirmwareContainer>`
   * - HDD
     - ``.hdd``
     - ...
     - :class:`here <dissect.target.containers.hdd.HddContainer>`
   * - HDS
     - ``.hds``
     - Parallels Desktop hard disk format
     - :class:`here <dissect.target.containers.hds.HdsContainer>`
   * - Qcow2
     - ``.qcow2``
     - Hard disk used for QEMU.
     - :class:`here <dissect.target.containers.qcow2.QCow2Container>`
   * - VDI
     - ``.vdi``
     - The virtualbox harddisk format.
     - :class:`here <dissect.target.containers.vdi.VdiContainer>`
   * - Virtual Hard Disk
     - ``.vhd``
     - ...
     - :class:`here <dissect.target.containers.vhd.VhdContainer>`
   * - Virtual Hard Disk X
     - ``.vhdx``
     - The virtual hard disk formats used for the Hyper-V hypervisor.
       VHD is a precursor to VHDX
     - :class:`here <dissect.target.containers.vhdx.VhdxContainer>`
   * - VMware disk format
     - ``.vmdk``
     - VMware virtual hard disks.
     - :class:`here <dissect.target.containers.vmdk.VmdkContainer>`

Partition Schemes and Volume Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Partitions organize a disk into multiple logical volumes.
Within `dissect.target` :class:`~dissect.target.volumes.disk.DissectVolumeSystem` handles the partition schemes that are listed below.

.. list-table:: Supported Partition Schemes
   :header-rows: 1
   :widths: 20

   * - Partition Scheme
   * - Apple Partition Map
     - :class:`<dissect.volume.disk.schemes.apm.APM>`
   * - BSD Disklabel
     - :class:`<dissect.volume.disk.schemes.bsd.BSD>`
   * - GUID Partition Table
     - :class:`<dissect.volume.disk.schemes.gpt.GPT>`
   * - Master Boot Record
     - :class:`<dissect.volume.disk.schemes.mbr.MBR>`

In addition to standard partition tables, Dissect supports various volume systems.
These are used for RAID configurations or encrypted volumes such as ``LUKS`` and ``BitLocker``.

.. seealso::

    For more details, see :doc:`volumes <advanced/volumes>`.

The table below lists the different supported volume systems.

.. list-table:: Supported Volume Systems
   :header-rows: 1
   :widths: 20 30

   * - Volume System
     - Description
   * - Bitlocker
     - :class:`<dissect.target.volumes.bde.BitlockerVolumeSystem>`
     - Bitlocker encrypted volume system. Used by windows systems
   * - Disk Data Format
     - :class:`<dissect.target.volumes.ddf.DdfVolumeSystem>`
     - DDF is a RAID data format that describes how data is formatted across raid groups.
   * - Linux Unified Key Setup
     - :class:`<dissect.target.volumes.luks.LUKSVolumeSystem>`
     - LUKS encrypted volume system. These are a standard specification for disk encryption on linux systems.
   * - Logical Volume Manager
     - :class:`<dissect.target.volumes.lvm.LvmVolumeSystem>`
     - LVM is a device mapper framework that can make multiple volumes on a single disk. 
   * - Multiple Device driver
     - :class:`<dissect.target.volumes.md.MdVolumeSystem>`
     - Linux MD RAID volume system. A software based RAID system.
   * - Virtual Machine Filesystem
     - :class:`<dissect.target.volumes.vmfs.VmfsVolumeSystem>`
     - VMFS is a clustered filesystem developed by VMWare on an ESXi type hosts.

Filesystems
~~~~~~~~~~~

In Dissect, filesystems go beyond traditional disk-based structures.
If it behaves like a filesystem, Dissect can likely treat it as one.
This includes both standard filesystems and formats that resemble filesystem behavior.

Dissect provides implementations for common filesystems such as :doc:`NTFS </projects/dissect.ntfs/index>` and :doc:`VMFS </projects/dissect.vmfs/index>`, as well as support for forensic formats, network shares, and virtual overlays.

.. seealso::

   For more details, see :doc:`Filesystems </advanced/filesystems>`.

.. list-table:: Supported Filesystems
   :header-rows: 1
   :widths: 20 30

   * - Filesystem
     - Description

   * - AD1
     - :class:`<dissect.target.filesystems.ad1.AD1Filesystem>`
     - Forensic container format (AccessData AD1).
   * - BTRFS
     - :class:`<dissect.target.filesystems.btrfs.BtrfsFilesystem>`
     - BTRFS filesystem with support for subvolumes.
   * - CpIO
     - :class:`<dissect.target.filesystems.cpio.CpioFilesystem>`
     - CPIO archive format.
   * - EXFAT
     - :class:`<dissect.target.filesystems.exfat.ExfatFilesystem>`
     - Microsoft EXFAT filesystem.
   * - Ext2, Ext3, Ext4
     - :class:`<dissect.target.filesystems.extfs.ExtFilesystem>`
     - Linux EXT family filesystems.
   * - FAT
     - :class:`<dissect.target.filesystems.fat.FatFilesystem>`
     - FAT12/16/32 filesystem.
   * - FFS
     - :class:`<dissect.target.filesystems.ffs.FfsFilesystem>`
     - Fast File System (BSD).
   * - JFFS
     - :class:`<dissect.target.filesystems.jffs.JffsFilesystem>`
     - Journaling Flash File System.
   * - Network File Share
     - :class:`<dissect.target.filesystems.nfs.NfsFilesystem>`
     - NFS share filesystem.
   * - NTFS
     - :class:`<dissect.target.filesystems.ntfs.NtfsFilesystem>`
     - Microsoft NTFS filesystem.
   * - Overlay2 <dissect.target.filesystems.overlay.Overlay2Filesystem>`, :class:`Overlay
     - :class:`<dissect.target.filesystems.overlay.OverlayFilesystem>`
     - Overlay filesystem used in container environments.
   * - QnxFs
     - :class:`<dissect.target.filesystems.qnxfs.QnxFilesystem>`
     - QNX filesystem.
   * - SquashFS
     - :class:`<dissect.target.filesystems.squashfs.SquashFSFilesystem>`
     - Compressed read-only filesystem.
   * - Virtual Backup Files
     - :class:`<dissect.target.filesystems.vbk.VbkFilesystem>`
     - Filesystem representation of VBK backup files.
   * - VMFS
     - :class:`<dissect.target.filesystems.vmfs.VmfsFilesystem>`
     - VMware VMFS filesystem.
   * - XFS
     - :class:`<dissect.target.filesystems.xfs.XfsFilesystem>`
     - High-performance journaling filesystem

Operating Systems
~~~~~~~~~~~~~~~~~

Dissect includes a range of ``OSPlugins`` that help identify the operating system present on a target.
These plugins analyze disk data to determine the system type, enabling more accurate queries such as retrieving user or network information.

Below is a list of supported operating systems that Dissect can detect.

.. list-table:: Supported Operating Systems
   :header-rows: 1
   :widths: 20

   * - Operating System
   * - Android
     - :class:`<dissect.target.plugins.os.unix.linux.android._os.AndroidPlugin>`
   * - Bsd
     - :class:`<dissect.target.plugins.os.unix.bsd._os.BsdPlugin>`
   * - Citrix
     - :class:`<dissect.target.plugins.os.unix.bsd.citrix._os.CitrixPlugin>`
   * - Darwin
     - :class:`<dissect.target.plugins.os.unix.bsd.darwin._os.DarwinPlugin>`
   * - Debian
     - :class:`<dissect.target.plugins.os.unix.linux.debian._os.DebianPlugin>`
   * - ESXi
     - :class:`<dissect.target.plugins.os.unix.esxi._os.ESXiPlugin>`
   * - Fortinet
     - :class:`<dissect.target.plugins.os.unix.linux.fortios._os.FortiOSPlugin>`
   * - FreeBSD
     - :class:`<dissect.target.plugins.os.unix.bsd.freebsd._os.FreeBsdPlugin>`
   * - iOS
     - :class:`<dissect.target.plugins.os.unix.bsd.darwin.ios._os.IOSPlugin>`
   * - Generic Linux
     - :class:`<dissect.target.plugins.os.unix.linux._os.LinuxPlugin>`
   * - MacOS
     - :class:`<dissect.target.plugins.os.unix.bsd.darwin.macos._os.MacOSPlugin>`
   * - OpenBSD
     - :class:`<dissect.target.plugins.os.unix.bsd.openbsd._os.OpenBsdPlugin>`
   * - Proxmox
     - :class:`<dissect.target.plugins.os.unix.linux.debian.proxmox._os.ProxmoxPlugin>`
   * - RedHat
     - :class:`<dissect.target.plugins.os.unix.linux.redhat._os.RedHatPlugin>`
   * - RES
     - :class:`<dissect.target.loaders.res.ResOSPlugin>`
   * - OpenSusSE
     - :class:`<dissect.target.plugins.os.unix.linux.suse._os.SuSEPlugin>`
   * - Unix
     - :class:`<dissect.target.plugins.os.unix._os.UnixPlugin>`
   * - Vyos
     - :class:`<dissect.target.plugins.os.unix.linux.debian.vyos._os.VyosPlugin>`
   * - Windows
     - :class:`<dissect.target.plugins.os.windows._os.WindowsPlugin>`

Child Targets
~~~~~~~~~~~~~

Dissect supports identifying, listing and querying *child targets*.
These are targets within other targets.
These can include virtual machines, containers, or other environments nested inside a target.
Child targets are discovered using configuration files or metadata present on the host or target.
Dissect can recursively query these targets, allowing it to detect deeply nested environments automatically.

.. seealso::

   For more details, see :ref:`Child targets <advanced/targets:Targets in targets>`.

.. list-table:: Supported Child Targets
   :header-rows: 1
   :widths: 15 35

   * - Child Target
     - Description
   * - Colima
     - :class:`<dissect.target.plugins.child.colima.ColimaChildTargetPlugin>`
     - Child target plugin that yields Colima containers.
   * - Docker
     - :class:`<dissect.target.plugins.child.docker.DockerChildTargetPlugin>`
     - Child target plugin that yields from Docker overlay2fs containers.
   * - ESXi
     - :class:`<dissect.target.plugins.child.esxi.ESXiChildTargetPlugin>`
     - Child target plugin that yields from ESXi VM inventory.
   * - Hyper-v
     - :class:`<dissect.target.plugins.child.hyperv.HyperVChildTargetPlugin>`
     - Child target plugin that yields from Hyper-V VM inventory.
   * - Lima
     - :class:`<dissect.target.plugins.child.lima.LimaChildTargetPlugin>`
     - Child target plugin that yields Lima VMs.
   * - Parallels
     - :class:`<dissect.target.plugins.child.parallels.ParallelsChildTargetPlugin>`
     - Child target plugin that yields Parallels Desktop VM files.
   * - Podman
     - :class:`<dissect.target.plugins.child.podman.PodmanChildTargetPlugin>`
     - Child target plugin that yields from Podman overlayfs containers
   * - Proxmox
     - :class:`<dissect.target.plugins.child.proxmox.ProxmoxChildTargetPlugin>`
     - Child target plugin that yields from the VM listing.
   * - Qemu
     - :class:`<dissect.target.plugins.child.qemu.QemuChildTargetPlugin>`
     - Child target plugin that yields all QEMU domains from a KVM libvirt deamon.
   * - VirtualBox
     - :class:`<dissect.target.plugins.child.virtualbox.VirtualBoxChildTargetPlugin>`
     - Child target plugin that yields from Oracle VirtualBox VMs.
   * - Virtuozzo
     - :class:`<dissect.target.plugins.child.virtuozzo.VirtuozzoChildTargetPlugin>`
     - Child target plugin that yields from Virtuozzo container's root.
   * - Vmware Workstation
     - :class:`<dissect.target.plugins.child.vmware_workstation.VmwareWorkstationChildTargetPlugin>`
     - Child target plugin that yields from VMware Workstation VM inventory.
   * - WSL
     - :class:`<dissect.target.plugins.child.wsl.WSLChildTargetPlugin>`
     - Child target plugin that yields Windos Subsystem Linux VHDX file locations.

