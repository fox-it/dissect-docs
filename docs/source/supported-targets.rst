Supported targets
-----------------

Dissect supports a large range of formats.
From various disk images, volume systems, file systems and operating systems, to tarballs and proprietary backup formats, and everything combined!
This page aims to provide you with an overview of what you can expect Dissect to be able to handle!

Loaders
~~~~~~~

Loaders provide a way to interact with a "target" by combining and accessing source data into usable parts.
This creates a virtual version of the original system.

.. seealso::

   For a deeper dive into how loaders work, see :doc:`loaders </advanced/loaders>`.

In most cases, Dissect selects the appropriate loader automatically based on the file you target.
It does this by looking at things like the file type, folder structure or special configurations files.
If needed, you can choose the loader yourself by using ``-L <loader type>`` option or by using the URI-style notation ``<loader type>://``.

.. code-block:: bash

   target-query -f func /path/to/target.ab
   target-query -f func -L ab /path/to/target
   target-query -f func ab:///path/to/target

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
   * - iTunes Backup
     - iTunes backup files. Only from a directory that contains a ``Manifest.plist`` file.
     -
     - :class:`itunes <dissect.target.loaders.itunes.ITunesLoader>`
   * - KAPE
     - KAPE forensic image format files. Only if the file or directory contains KAPE specific directories.
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

Containers let Dissect interact with a disk-like structure in a consistent way.
These can be virtual machine files, forensic containers or a hard disk itself.

.. seealso::

   For a deeper understanding on how containers work, see :doc:`containers <advanced/containers>`.

The table below lists the supported container formats.

.. list-table:: Supported Containers
   :header-rows: 1
   :widths: 20 20 5 5

   * - Container
     - Description
     - Extension
     - API
   * - Apple Sparse Image Format
     - A sparse disk format introduced by Apple with near native SSD speeds.
     - ``.asif``
     - :class:`here <dissect.target.containers.asif.AsifContainer>`
   * - Expert Witness Disk Image Format
     - FTK Expert witness data format.
     - ``.E01``, ``.L01``, ``.Ex01``, ``.Lx01`` 
     - :class:`here <dissect.target.containers.ewf.EwfContainer>`
   * - Fortinet Firmware
     - Interprets and decompresses a Fortinet firmware file.
     - ``*-fortinet.out``
     - :class:`here <dissect.target.containers.fortifw.FortiFirmwareContainer>`
   * - HDD
     - Parallels HDD virtual disk implementation.
     - ``.hdd``
     - :class:`here <dissect.target.containers.hdd.HddContainer>`
   * - HDS
     - Parallels sparse hard disk format
     - ``.hds``
     - :class:`here <dissect.target.containers.hds.HdsContainer>`
   * - Qcow2
     - QEMU Copy On Write virtual disk format.
     - ``.qcow2``
     - :class:`here <dissect.target.containers.qcow2.QCow2Container>`
   * - VDI
     - The virtualbox harddisk format.
     - ``.vdi``
     - :class:`here <dissect.target.containers.vdi.VdiContainer>`
   * - Virtual Hard Disk
     - The original virtual hard disk format developed by Microsoft. Mainly used by the Hyper-V hypervisor.
     - ``.vhd``
     - :class:`here <dissect.target.containers.vhd.VhdContainer>`
   * - Virtual Hard Disk X
     - Virtual Hard Disk v2, the successor of VHD, and the new default on Hyper-V.
     - ``.vhdx``
     - :class:`here <dissect.target.containers.vhdx.VhdxContainer>`
   * - VMware disk format
     - VMware virtual hard disks.
     - ``.vmdk``
     - :class:`here <dissect.target.containers.vmdk.VmdkContainer>`

Partition Schemes and Volume Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dissect supports the following partition schemes to divide a disk into multiple logical volumes.

.. list-table:: Supported Partition Schemes
   :header-rows: 1
   :widths: 45 5

   * - Partition Scheme
     - API
   * - Apple Partition Map
     - :class:`here <dissect.volume.disk.schemes.apm.APM>`
   * - BSD Disklabel
     - :class:`here <dissect.volume.disk.schemes.bsd.BSD>`
   * - GUID Partition Table
     - :class:`here <dissect.volume.disk.schemes.gpt.GPT>`
   * - Master Boot Record
     - :class:`here <dissect.volume.disk.schemes.mbr.MBR>`

Besides these standard partition tables used in most computer systems, Dissect supports disks in RAID configurations or disks with logical volumes that span multiple disks.

.. seealso::

    For more details, see :doc:`volumes <advanced/volumes>`.

The table below lists the different supported volume systems.

.. list-table:: Supported Volume Systems
   :header-rows: 1
   :widths: 20 30 5

   * - Volume System
     - Description
     - API
   * - Disk Data Format
     - DDF is a RAID data format that describes how data is formatted across raid groups.
     - :class:`here <dissect.target.volumes.ddf.DdfVolumeSystem>`
   * - Logical Volume Manager
     - LVM is a device mapper framework that can make multiple volumes on a single disk.
     - :class:`here <dissect.target.volumes.lvm.LvmVolumeSystem>`
   * - Multiple Device driver
     - Linux MD RAID volume system. A software based RAID system.
     - :class:`here <dissect.target.volumes.md.MdVolumeSystem>`
   * - Virtual Machine Filesystem
     - VMFS is a clustered filesystem developed by VMWare on an ESXi type hosts.
     - :class:`here <dissect.target.volumes.vmfs.VmfsVolumeSystem>`

Dissect also has decryption capability for some well known systems.
This functionality can be accessed with a keychain file (specified with ``-K``) with multiple passphrases or a keychain value (``-Kv``) in most Dissect tools.
Dissect supports the following encryption formats.

.. list-table:: Supported Encrypted Volume Systems
   :header-rows: 1
   :widths: 20 30 5

   * - Encrypted volume system
     - Description
     - API
   * - Linux Unified Key Setup
     - LUKS encrypted volume system. These are the standard specification for disk encryption on linux systems.
     - :class:`here <dissect.target.volumes.luks.LUKSVolumeSystem>`
   * - BitLocker
     - BitLocker encrypted volume system. Used by Windows systems
     - :class:`here <dissect.target.volumes.bde.BitlockerVolumeSystem>`

Filesystems
~~~~~~~~~~~

In Dissect, filesystems go beyond traditional disk-based structures.
If it behaves like a filesystem, Dissect can likely treat it as one.
This includes both standard filesystems and formats that resemble filesystem behavior.

.. seealso::

   For more details, see :doc:`Filesystems </advanced/filesystems>`.

.. list-table:: Supported Filesystems
   :header-rows: 1
   :widths: 20 30 5

   * - Filesystem
     - Description
     - API
   * - AD1
     - Forensic container format (AccessData AD1).
     - :class:`here <dissect.target.filesystems.ad1.AD1Filesystem>`
   * - APFS
     - Apple Filesystem.
     - :class:`here <dissect.target.filesystems.apfs.ApfsFilesystem>`
   * - BTRFS
     - Binary-tree file system with support for subvolumes.
     - :class:`here <dissect.target.filesystems.btrfs.BtrfsFilesystem>`
   * - CPIO
     - CPIO archive format.
     - :class:`here <dissect.target.filesystems.cpio.CpioFilesystem>`
   * - exFAT
     - Microsoft Extensible File Allocation Table filesystem.
     - :class:`here <dissect.target.filesystems.exfat.ExfatFilesystem>`
   * - Ext2, Ext3, Ext4
     - Linux EXT family filesystems.
     - :class:`here <dissect.target.filesystems.extfs.ExtFilesystem>`
   * - FAT
     - File Allocation Table 12/16/32-bit filesystem.
     - :class:`here <dissect.target.filesystems.fat.FatFilesystem>`
   * - FFS
     - Fast Filesystem (BSD).
     - :class:`here <dissect.target.filesystems.ffs.FfsFilesystem>`
   * - JFFS
     - Journaling Flash Filesystem.
     - :class:`here <dissect.target.filesystems.jffs.JffsFilesystem>`
   * - NFS
     - Network File Share filesystem. Gives the ability to connect to an NFS share
     - :class:`here <dissect.target.filesystems.nfs.NfsFilesystem>`
   * - NTFS
     - Microsoft NT Filesystem.
     - :class:`here <dissect.target.filesystems.ntfs.NtfsFilesystem>`
   * - Overlay
     - Overlay filesystem combines multiple layers into one singular filesystem. This filesystem is used for container formats for Docker or Podman.
     - :class:`here <dissect.target.filesystems.overlay.OverlayFilesystem>`
   * - Overlay2
     - Overlay2 Filesystem is a more efficient version of the Overlay filesystem.
     - :class:`here <dissect.target.filesystems.overlay.Overlay2Filesystem>`
   * - QNX4, QNX6
     - QNX filesystem, commonly used in the QNX RTOS.
     - :class:`here <dissect.target.filesystems.qnxfs.QnxFilesystem>`
   * - SquashFS
     - Compressed read-only filesystem used by linux systems.
     - :class:`here <dissect.target.filesystems.squashfs.SquashFSFilesystem>`
   * - Virtual Backup Files
     - Filesystem representation of VBK backup files.
     - :class:`here <dissect.target.filesystems.vbk.VbkFilesystem>`
   * - VMFS
     - VMware VMFS filesystem.
     - :class:`here <dissect.target.filesystems.vmfs.VmfsFilesystem>`
   * - XFS
     - High-performance journaling filesystem
     - :class:`here <dissect.target.filesystems.xfs.XfsFilesystem>`

Operating Systems
~~~~~~~~~~~~~~~~~

Dissect supports various operating systems, where Dissect tries to automatically figure out what operating system is available on the disk.
Once the operating system is known, it enables the user to get more accurate information from the system, for example, the user or network configuration.

Below is a list of supported operating systems that Dissect can detect.

.. list-table:: Supported Operating Systems
   :header-rows: 1
   :widths: 45 5

   * - Operating System
     - API
   * - Windows
     - :class:`here <dissect.target.plugins.os.windows._os.WindowsPlugin>`
   * - Unix
     - :class:`here <dissect.target.plugins.os.unix._os.UnixPlugin>`
   * - ESXi
     - :class:`here <dissect.target.plugins.os.unix.esxi._os.ESXiPlugin>`
   * - BSD
     - :class:`here <dissect.target.plugins.os.unix.bsd._os.BsdPlugin>`
   * - Citrix
     - :class:`here <dissect.target.plugins.os.unix.bsd.citrix._os.CitrixPlugin>`
   * - FreeBSD
     - :class:`here <dissect.target.plugins.os.unix.bsd.freebsd._os.FreeBsdPlugin>`
   * - OpenBSD
     - :class:`here <dissect.target.plugins.os.unix.bsd.openbsd._os.OpenBsdPlugin>`
   * - Darwin
     - :class:`here <dissect.target.plugins.os.unix.bsd.darwin._os.DarwinPlugin>`
   * - iOS
     - :class:`here <dissect.target.plugins.os.unix.bsd.darwin.ios._os.IOSPlugin>`
   * - macOS
     - :class:`here <dissect.target.plugins.os.unix.bsd.darwin.macos._os.MacOSPlugin>`
   * - Generic Linux
     - :class:`here <dissect.target.plugins.os.unix.linux._os.LinuxPlugin>`
   * - Android
     - :class:`here <dissect.target.plugins.os.unix.linux.android._os.AndroidPlugin>`
   * - FortiOS
     - :class:`here <dissect.target.plugins.os.unix.linux.fortios._os.FortiOSPlugin>`
   * - OpenSUSE
     - :class:`here <dissect.target.plugins.os.unix.linux.suse._os.SuSEPlugin>`
   * - RedHat
     - :class:`here <dissect.target.plugins.os.unix.linux.redhat._os.RedHatPlugin>`
   * - Debian
     - :class:`here <dissect.target.plugins.os.unix.linux.debian._os.DebianPlugin>`
   * - Proxmox
     - :class:`here <dissect.target.plugins.os.unix.linux.debian.proxmox._os.ProxmoxPlugin>`
   * - VyOS
     - :class:`here <dissect.target.plugins.os.unix.linux.debian.vyos._os.VyosPlugin>`

Child Targets
~~~~~~~~~~~~~

Dissect supports identifying, listing and querying *child targets*.
These are systems within other systems and can include virtual machines, containers or any other environment inside a "target".
Dissect finds these systems by looking inside configuration files on the systems.
It can even look deeper, and look inside those systems within systems for even more *child targets*.

.. seealso::

   For more details, see :ref:`Child targets <advanced/targets:Targets in targets>`.

.. list-table:: Supported Child Targets
   :header-rows: 1
   :widths: 15 35 5

   * - Child Target
     - Description
     - API
   * - Colima
     - Colima container format, which is a runtime for both Linux and macOS.
     - :class:`here <dissect.target.plugins.child.colima.ColimaChildTargetPlugin>`
   * - Docker
     - The Docker overlay2fs containers that are available on the system.
     - :class:`here <dissect.target.plugins.child.docker.DockerChildTargetPlugin>`
   * - ESXi
     - The VM inventory on ESXi machines.
     - :class:`here <dissect.target.plugins.child.esxi.ESXiChildTargetPlugin>`
   * - Hyper-V
     - The VM inventory on Hyper-V Windows hosts.
     - :class:`here <dissect.target.plugins.child.hyperv.HyperVChildTargetPlugin>`
   * - Lima
     - Lima, Linux Machines, is a container / VM runtime that supports different container engines such as Docker, Podman, and Kubernetes.
     - :class:`here <dissect.target.plugins.child.lima.LimaChildTargetPlugin>`
   * - Parallels
     - The Parallels Desktop inventory, Parallels is a hypervisor for Mac computers.
     - :class:`here <dissect.target.plugins.child.parallels.ParallelsChildTargetPlugin>`
   * - Podman
     - Podman, a container runtime engine such as Docker.
     - :class:`here <dissect.target.plugins.child.podman.PodmanChildTargetPlugin>`
   * - Proxmox
     - Proxmox is a debian based virtualization platform.
     - :class:`here <dissect.target.plugins.child.proxmox.ProxmoxChildTargetPlugin>`
   * - QEMU
     - All QEMU virtual machines created by the KVM libvirt deamon.
     - :class:`here <dissect.target.plugins.child.qemu.QemuChildTargetPlugin>`
   * - VirtualBox
     - Oracle VirtualBox VMs.
     - :class:`here <dissect.target.plugins.child.virtualbox.VirtualBoxChildTargetPlugin>`
   * - Virtuozzo
     - All the Virtuozzo containers.
     - :class:`here <dissect.target.plugins.child.virtuozzo.VirtuozzoChildTargetPlugin>`
   * - VMware Workstation
     - All the VMs registerd within the VMware Workstation VM inventory.
     - :class:`here <dissect.target.plugins.child.vmware_workstation.VmwareWorkstationChildTargetPlugin>`
   * - WSL2
     - All the Windows Subsystem for Linux 2 instances.
     - :class:`here <dissect.target.plugins.child.wsl.WSLChildTargetPlugin>`

