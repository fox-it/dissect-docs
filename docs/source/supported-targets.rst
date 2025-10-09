Supported targets
-----------------

Dissect supports a large range of formats. From various disk images, volume systems, file systems and operating systems, to tarballs and proprietary backup formats, and everything combined! This page aims to provide you with an overview of what you can expect Dissect to be able to handle!

Loaders
~~~~~~~

Loaders provide a way to interact with a "target" by combining and accessing source data into usable components for ``dissect.target``.
The goal is to build a virtual representation of the original system.

.. seealso::

   For a deeper dive into how loaders work, see :doc:`loaders </advanced/loaders>`.

In most cases, the appropriate loader is selected automatically based on the target.
However, you can also specify a loader manually using the ``-L <loader type>`` flag or URI-style notation ``<loader type>://``.

.. code-block:: bash

   target-query -f func -L ab /path/to/target
   target-query -f func ab:///path/to/target

.. list-table:: Supported Loaders
   :header-rows: 1
   :widths: 15 10 25

   * - Name
     - Loader type
     - Description
   * - :class:`Android Backup <dissect.target.loaders.ab.AndroidBackupLoader>`
     - ``ab``
     - Load Android backup files.
   * - :class:`Carbon Black <dissect.target.loaders.cb.CbLoader>`
     - ``cb``
     - Carbon Black Live Response endpoints. Can only be used directly with ``cb://`` or ``-L cb``.
   * - :class:`Cellebrite <dissect.target.loaders.cellebrite.CellebriteLoader>`
     - ``cellebrite``
     - Load Cellebrite UFED exports (``.ufdx`` and ``.ufd``).
   * - :class:`Directory <dissect.target.loaders.dir.DirLoader>`
     - ``dir``
     - Load a local directory as a filesystem.
   * - :class:`Hyper-V <dissect.target.loaders.hyperv.HyperVLoader>`
     - ``hyperv``
     - Load Microsoft Hyper-V hypervisor files.
   * - :class:`Itunes Backup <dissect.target.loaders.itunes.ITunesLoader>`
     - ``itunes``
     - Load iTunes backup files.
   * - :class:`Kape <dissect.target.loaders.kape.KapeLoader>`
     - ``kape``
     - Load KAPE forensic image format files.
   * - :class:`Libvirt <dissect.target.loaders.libvirt.LibvirtLoader>`
     - ``libvirt``
     - Load libvirt xml configuration files.
   * - :class:`Local <dissect.target.loaders.local.LocalLoader>`
     - ``local``.
     - Load local filesystem.
   * - :class:`Log <dissect.target.loaders.log.LogLoader>`
     - ``log``
     - Load separate log files without a target.
   * - :class:`MQTT <dissect.target.loaders.mqtt.MqttLoader>`
     - ``mqtt``
     - Load remote targets through a mqtt broker.
   * - :class:`OVA <dissect.target.loaders.ova.OvaLoader>`
     - ``ova``
     - Load Open Virtual Appliance (OVA) files.
   * - :class:`Overlay2 <dissect.target.loaders.overlay2.Overlay2Loader>`

       :class:`Overlay <dissect.target.loaders.overlay.OverlayLoader>`
     - ``overlay2``, ``overlay``
     - Load the different layers of a docker container image.
   * - :class:`Open Virtualization Format <dissect.target.loaders.ovf.OvfLoader>`
     - ``ovf``
     - Load Open Virtualization Format (OVF) files.
   * - :class:`Phobos <dissect.target.loaders.phobos.PhobosLoader>`
     - ``phobos``
     - Load Phobos Ransomware files.
   * - :class:`Proxmox <dissect.target.loaders.proxmox.ProxmoxLoader>`
     - ``proxmox``
     - Loader for Proxmox VM configuration files.
   * - :class:`Parallels VM <dissect.target.loaders.pvm.PvmLoader>`

       :class:`Parallels VM Configuration <dissect.target.loaders.pvs.PvsLoader>`
     - ``pvm``, ``pvs``
     - Parallels VM directory (.pvm) and the conviguration file (config.pvs)
   * - :class:`Raw <dissect.target.loaders.raw.RawLoader>`

       :class:`MultiRaw <dissect.target.loaders.multiraw.MultiRawLoader>`
     - ``raw``, ``multiraw``
     - Load raw container files such as disk images.
       To load multiple raw containers in a single target, use ``MultiRaw``.
       To use this loader automatically use ``+`` to chain disks. E.g. ``/dev/vda+/dev/vdb`` 
   * - :class:`Remote <dissect.target.loaders.remote.RemoteLoader>`
     - ``remote``
     - Load a remote target that runs a compatible Dissect agent.
   * - :class:`SMB <dissect.target.loaders.smb.SmbLoader>`
     - ``smb``
     - Use an SMB connection to user remote SMB servers as a target.
       This particular loader requires ``impacket`` to be installed.
   * - :class:`Tanium <dissect.target.loaders.tanium.TaniumLoader>`
     - ``tanium``
     - Load Tanium forensic image format files.
   * - :class:`Tar <dissect.target.loaders.tar.TarLoader>`
     - ``tar``
     - Load tar files, docker container images and output files from Acquire or UAC.
   * - :class:`Target <dissect.target.loaders.target.TargetLoader>`
     - ``target``
     - Load target system using a target file.
   * - :class:`Unix-like Artifacts Collector <dissect.target.loaders.uac.UacLoader>`
     - ``uac``
     - Load the output of the UAC tool
   * - :class:`UTM <dissect.target.loaders.utm.UtmLoader>`
     - ``utm``
     - Load UTM virtual machine files.
   * - :class:`VB <dissect.target.loaders.vb.VBLoader>`
     - ``vb``
     - No documentation
   * - :class:`Virtual Box <dissect.target.loaders.vbox.VBoxLoader>`
     - ``vbox``
     - Load Oracle VirtualBox files.
   * - :class:`Veaam Backup <dissect.target.loaders.vbk.VbkLoader>`
     - ``vbk``
     - Load Veaam Backup (VBK) files.
   * - :class:`Velociraptor <dissect.target.loaders.velociraptor.VelociraptorLoader>`
     - ``velociraptor``
     - Load Rapid7 Velociraptor forensic image files.
   * - :class:`Virtual Machine Archive <dissect.target.loaders.vma.VmaLoader>`
     - ``vma``
     - Load Proxmox Virtual Machine Archive (VMA) files.
   * - :class:`VMware Fusion <dissect.target.loaders.vmwarevm.VmwarevmLoader>`
     - ``vmwarevm``
     - Load ``*.vmwarevm`` folders from VMware Fusion.
   * - :class:`VMware VM configuration <dissect.target.loaders.vmx.VmxLoader>`
     - ``vmx``
     - Load VMware virtual machine configuration (VMX) files.
   * - :class:`XVA <dissect.target.loaders.xva.XvaLoader>`
     - ``xva``
     - Load Citrix Hypervisor XVA format files.
   * - :class:`Zip <dissect.target.loaders.zip.ZipLoader>`
     - ``zip``
     - Load zip files themselves or interpret the output of tools like Acquire or UAC.

Containers
~~~~~~~~~~

Containers are the abstraction layer for anything that looks (or should look) like a raw disk.
They allow Dissect to interpret and interact with disk-like data structures in a consistent way.

.. seealso::

   For a deeper understanding on how containers work, see :doc:`containers <advanced/containers>`.

The table below lists the supported container formats.

.. list-table:: Supported Containers
   :header-rows: 1
   :widths: 20 30

   * - Container
     - Description
   * - :class:`Apple Sparse Image Format <dissect.target.containers.asif.AsifContainer>`
     - No Documentation
   * - :class:`Expert Witness Disk Image Format <dissect.target.containers.ewf.EwfContainer>`
     - Expert Witness Disk Image Format.
   * - :class:`Fortinet Firmware <dissect.target.containers.fortifw.FortiFirmwareContainer>`
     - No documentation
   * - :class:`HDD<dissect.target.containers.hdd.HddContainer>`

       :class:`HDS <dissect.target.containers.hds.HdsContainer>`
     - Parallels Desktop hard disk format
   * - :class:`Qcow2 <dissect.target.containers.qcow2.QCow2Container>`
     - Hard disk used for QEMU.
   * - :class:`VDI <dissect.target.containers.vdi.VdiContainer>`
     - The virtualbox harddisk format.
   * - :class:`Virtual Hard Disk <dissect.target.containers.vhd.VhdContainer>`

       :class:`Virtual Hard Disk X <dissect.target.containers.vhdx.VhdxContainer>`
     - The virtual hard disk formats used for the Hyper-V hypervisor.
       VHD is a precursor to VHDX
   * - :class:`VMware disk format <dissect.target.containers.vmdk.VmdkContainer>`
     - VMware virtual hard disks.

Partition Schemes and Volume Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Partitions organize a disk into multiple logical volumes.
Within `dissect.target` :class:`~dissect.target.volumes.disk.DissectVolumeSystem` handles the partition schemes that are listed below.

.. list-table:: Supported Partition Schemes
   :header-rows: 1
   :widths: 20

   * - Partition Scheme
   * - :class:`Apple Partition Map <dissect.volume.disk.schemes.apm.APM>`
   * - :class:`BSD Disklabel <dissect.volume.disk.schemes.bsd.BSD>`
   * - :class:`GUID Partition Table <dissect.volume.disk.schemes.gpt.GPT>`
   * - :class:`Master Boot Record <dissect.volume.disk.schemes.mbr.MBR>`

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
   * - :class:`Bitlocker <dissect.target.volumes.bde.BitlockerVolumeSystem>`
     - Bitlocker encrypted volume system. Used by windows systems
   * - :class:`Disk Data Format <dissect.target.volumes.ddf.DdfVolumeSystem>`
     - DDF is a RAID data format that describes how data is formatted across raid groups.
   * - :class:`Linux Unified Key Setup <dissect.target.volumes.luks.LUKSVolumeSystem>`
     - LUKS encrypted volume system. These are a standard specification for disk encryption on linux systems.
   * - :class:`Logical Volume Manager <dissect.target.volumes.lvm.LvmVolumeSystem>`
     - LVM is a device mapper framework that can make multiple volumes on a single disk. 
   * - :class:`Multiple Device driver <dissect.target.volumes.md.MdVolumeSystem>`
     - Linux MD RAID volume system. A software based RAID system.
   * - :class:`Virtual Machine Filesystem <dissect.target.volumes.vmfs.VmfsVolumeSystem>`
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

   * - :class:`AD1 <dissect.target.filesystems.ad1.AD1Filesystem>`
     - Forensic container format (AccessData AD1).
   * - :class:`BTRFS <dissect.target.filesystems.btrfs.BtrfsFilesystem>`
     - BTRFS filesystem with support for subvolumes.
   * - :class:`CpIO <dissect.target.filesystems.cpio.CpioFilesystem>`
     - CPIO archive format.
   * - :class:`EXFAT <dissect.target.filesystems.exfat.ExfatFilesystem>`
     - Microsoft EXFAT filesystem.
   * - :class:`Ext2, Ext3, Ext4 <dissect.target.filesystems.extfs.ExtFilesystem>`
     - Linux EXT family filesystems.
   * - :class:`FAT <dissect.target.filesystems.fat.FatFilesystem>`
     - FAT12/16/32 filesystem.
   * - :class:`FFS <dissect.target.filesystems.ffs.FfsFilesystem>`
     - Fast File System (BSD).
   * - :class:`JFFS <dissect.target.filesystems.jffs.JffsFilesystem>`
     - Journaling Flash File System.
   * - :class:`Network File Share <dissect.target.filesystems.nfs.NfsFilesystem>`
     - NFS share filesystem.
   * - :class:`NTFS <dissect.target.filesystems.ntfs.NtfsFilesystem>`
     - Microsoft NTFS filesystem.
   * - :class:`Overlay2 <dissect.target.filesystems.overlay.Overlay2Filesystem>`, :class:`Overlay <dissect.target.filesystems.overlay.OverlayFilesystem>`
     - Overlay filesystem used in container environments.
   * - :class:`QnxFs <dissect.target.filesystems.qnxfs.QnxFilesystem>`
     - QNX filesystem.
   * - :class:`SquashFS <dissect.target.filesystems.squashfs.SquashFSFilesystem>`
     - Compressed read-only filesystem.
   * - :class:`Virtual Backup Files <dissect.target.filesystems.vbk.VbkFilesystem>`
     - Filesystem representation of VBK backup files.
   * - :class:`VMFS <dissect.target.filesystems.vmfs.VmfsFilesystem>`
     - VMware VMFS filesystem.
   * - :class:`XFS <dissect.target.filesystems.xfs.XfsFilesystem>`
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
   * - :class:`Android <dissect.target.plugins.os.unix.linux.android._os.AndroidPlugin>`
   * - :class:`Bsd <dissect.target.plugins.os.unix.bsd._os.BsdPlugin>`
   * - :class:`Citrix <dissect.target.plugins.os.unix.bsd.citrix._os.CitrixPlugin>`
   * - :class:`Darwin <dissect.target.plugins.os.unix.bsd.darwin._os.DarwinPlugin>`
   * - :class:`Debian <dissect.target.plugins.os.unix.linux.debian._os.DebianPlugin>`
   * - :class:`ESXi <dissect.target.plugins.os.unix.esxi._os.ESXiPlugin>`
   * - :class:`Fortinet <dissect.target.plugins.os.unix.linux.fortios._os.FortiOSPlugin>`
   * - :class:`FreeBSD <dissect.target.plugins.os.unix.bsd.freebsd._os.FreeBsdPlugin>`
   * - :class:`iOS <dissect.target.plugins.os.unix.bsd.darwin.ios._os.IOSPlugin>`
   * - :class:`Generic Linux <dissect.target.plugins.os.unix.linux._os.LinuxPlugin>`
   * - :class:`MacOS <dissect.target.plugins.os.unix.bsd.darwin.macos._os.MacOSPlugin>`
   * - :class:`OpenBSD <dissect.target.plugins.os.unix.bsd.openbsd._os.OpenBsdPlugin>`
   * - :class:`Proxmox <dissect.target.plugins.os.unix.linux.debian.proxmox._os.ProxmoxPlugin>`
   * - :class:`RedHat <dissect.target.plugins.os.unix.linux.redhat._os.RedHatPlugin>`
   * - :class:`RES <dissect.target.loaders.res.ResOSPlugin>`
   * - :class:`OpenSusSE <dissect.target.plugins.os.unix.linux.suse._os.SuSEPlugin>`
   * - :class:`Unix <dissect.target.plugins.os.unix._os.UnixPlugin>`
   * - :class:`Vyos <dissect.target.plugins.os.unix.linux.debian.vyos._os.VyosPlugin>`
   * - :class:`Windows <dissect.target.plugins.os.windows._os.WindowsPlugin>`

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
   * - :class:`Colima <dissect.target.plugins.child.colima.ColimaChildTargetPlugin>`
     - Child target plugin that yields Colima containers.
   * - :class:`Docker <dissect.target.plugins.child.docker.DockerChildTargetPlugin>`
     - Child target plugin that yields from Docker overlay2fs containers.
   * - :class:`ESXi <dissect.target.plugins.child.esxi.ESXiChildTargetPlugin>`
     - Child target plugin that yields from ESXi VM inventory.
   * - :class:`Hyper-v <dissect.target.plugins.child.hyperv.HyperVChildTargetPlugin>`
     - Child target plugin that yields from Hyper-V VM inventory.
   * - :class:`Lima <dissect.target.plugins.child.lima.LimaChildTargetPlugin>`
     - Child target plugin that yields Lima VMs.
   * - :class:`Parallels <dissect.target.plugins.child.parallels.ParallelsChildTargetPlugin>`
     - Child target plugin that yields Parallels Desktop VM files.
   * - :class:`Podman <dissect.target.plugins.child.podman.PodmanChildTargetPlugin>`
     - Child target plugin that yields from Podman overlayfs containers
   * - :class:`Proxmox <dissect.target.plugins.child.proxmox.ProxmoxChildTargetPlugin>`
     - Child target plugin that yields from the VM listing.
   * - :class:`Qemu <dissect.target.plugins.child.qemu.QemuChildTargetPlugin>`
     - Child target plugin that yields all QEMU domains from a KVM libvirt deamon.
   * - :class:`VirtualBox <dissect.target.plugins.child.virtualbox.VirtualBoxChildTargetPlugin>`
     - Child target plugin that yields from Oracle VirtualBox VMs.
   * - :class:`Virtuozzo <dissect.target.plugins.child.virtuozzo.VirtuozzoChildTargetPlugin>`
     - Child target plugin that yields from Virtuozzo container's root.
   * - :class:`Vmware Workstation <dissect.target.plugins.child.vmware_workstation.VmwareWorkstationChildTargetPlugin>`
     - Child target plugin that yields from VMware Workstation VM inventory.
   * - :class:`WSL <dissect.target.plugins.child.wsl.WSLChildTargetPlugin>`
     - Child target plugin that yields Windos Subsystem Linux VHDX file locations.

