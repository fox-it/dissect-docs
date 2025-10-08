Supported targets
-----------------

This page contains a list of the systems that ``dissect`` supports.

Loaders
~~~~~~~

Loaders are a method to interact with a <target>.
They are responsible for mapping any kind of source data into something ``dissect.target`` understands.
They do this by stitching together different files to construct a virtual representation of the system.

.. seealso::

    See :doc:`loaders </advanced/loaders>` for more information about how they work.

The table below shows the different kind of loaders we have.
Most of these loaders are selected automatically based on the type of targets.
However you can access most of them using directly using ``-L <loader type>`` or use URI notation ``<loader type>://``.
E.g. for the ``Android Backup`` loader you use either

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
     - Use Carbon Black endpoints as targets using Live Response.
   * - :class:`Cellebrite <dissect.target.loaders.cellebrite.CellebriteLoader>`
     - ``cellebrite``
     - Load Cellebrite UFED exports (``.ufdx`` and ``.ufd``).
   * - :class:`Directory <dissect.target.loaders.dir.DirLoader>`
     - ``dir``
     - Load a local directory as a filesystem.
   * - :class:`Direct <dissect.target.loaders.direct.DirectLoader>`
     - ``--direct``
     - Load an evidence file directly instead of an image format.
       The plugins that can be used with this loader are:

       - apache
       - evt
       - evtx
       - iis
       - syslog
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
     - Parallels VM directory (.pvm).
       Parallels VM configuration file (config.pvs).
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
     - Load tar output files from a variety of tools. These can be the outputs of files.
         - Acquire
         - Docker
         - UAC
   * - :class:`Target <dissect.target.loaders.target.TargetLoader>`
     - ``target``
     - Load target system using a target file.
   * - :class:`Unix-like Artifacts Collector <dissect.target.loaders.uac.UacLoader>` .. todo
     - ``uac``
     - Load the output of the UAC tool
   * - :class:`UTM <dissect.target.loaders.utm.UtmLoader>` .. todo
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
     - Load zip output files from a variety of tools. These can be the outputs of files.
         - Acquire
         - UAC


Containers
~~~~~~~~~~

Containers are the abstraction layer for anything that looks (or should look) like a raw disk. Look at ``containers`` for more information about them.


.. list-table:: Supported Containers
   :header-rows: 1
   :widths: 15 35

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

Partitions organize a disk into multiple logical disks. The volume system abstraction inside `dissect.target` takes care of these partition schemes with the :class:`~dissect.target.volumes.disk.DissectVolumeSystem`.

.. seealso::

    See :doc:`volumes <advanced/volumes>` for more information about volume systems inside dissect.

.. list-table:: Supported Partition Schemes
   :header-rows: 1
   :widths: 15 35

   * - Partition Scheme
     - Description
   * - :class:`Apple Partition Map <dissect.volume.disk.schemes.apm.APM>`
     - Apple Partition Map.
   * - :class:`BSD Disklabel <dissect.volume.disk.schemes.bsd.BSD>`
     - BSD disklabel.
   * - :class:`GUID Partition Table <dissect.volume.disk.schemes.gpt.GPT>`
     - GUID Partition Table.
   * - :class:`Master Boot Record <dissect.volume.disk.schemes.mbr.MBR>`
     - Master Boot Record.

.. list-table:: Supported Volume Systems
   :header-rows: 1
   :widths: 15 35

   * - Volume System
     - Description
   * - :class:`Bitlocker <dissect.target.volumes.bde.BitlockerVolumeSystem>`
     - The bitlocker encrypted volume system.
   * - :class:`DDF <dissect.target.volumes.ddf.DdfVolumeSystem>`
     - No documentation
   * - :class:`LUKS <dissect.target.volumes.luks.LUKSVolumeSystem>`
     - No documentation
   * - :class:`Logical Volume Manager <dissect.target.volumes.lvm.LvmVolumeSystem>`
     - No documentation
   * - :class:`MD <dissect.target.volumes.md.MdVolumeSystem>`
     - A raid volume system
   * - :class:`VMFS <dissect.target.volumes.vmfs.VmfsVolumeSystem>`
     - No documentation

Filesystems
~~~~~~~~~~~

In Dissect, filesystems are a lot more than *actual* filesystems on a disk.
Because if you squint hard enough, almost anything can be a filesystem!
Dissect has various *real* filesystem implementations, such as :doc:`/projects/dissect.ntfs/index` or :doc:`/projects/dissect.vmfs/index`, but Dissect also supports a lot of other things that *resemble* a filesystem.

.. seealso::

   See :doc:`filesystems </advanced/filesystems>` for more information.

.. list-table:: Supported Filesystems
   :header-rows: 1
   :widths: 15 30

   * - Filesystem
     - Description
   * - :class:`AD1 <dissect.target.filesystems.ad1.AD1Filesystem>`
     - A filesystem representation of the AD1 forensic format.
   * - :class:`BTRFS <dissect.target.filesystems.btrfs.BtrfsFilesystem>`
     - An implementation for the BTRFS, this also includes any subvolumes on a BTRFS system.
   * - :class:`CpIO <dissect.target.filesystems.cpio.CpioFilesystem>`
     - No documentation
   * - :class:`EXFAT <dissect.target.filesystems.exfat.ExfatFilesystem>`
     - No documentation
   * - :class:`Ext2, Ext3, Ext4 <dissect.target.filesystems.extfs.ExtFilesystem>`
     - No documentation
   * - :class:`Fat <dissect.target.filesystems.fat.FatFilesystem>`
     - No documentation
   * - :class:`FFS <dissect.target.filesystems.ffs.FfsFilesystem>`
     - No documentation
   * - :class:`JFFS <dissect.target.filesystems.jffs.JffsFilesystem>`
     - No documentation
   * - :class:`Network File Share <dissect.target.filesystems.nfs.NfsFilesystem>`
     - Filesystem implementation of a NFS share
   * - :class:`NTFS <dissect.target.filesystems.ntfs.NtfsFilesystem>`
     - No documentation
   * - :class:`Overlay2 <dissect.target.filesystems.overlay.Overlay2Filesystem>`

       :class:`Overlay <dissect.target.filesystems.overlay.OverlayFilesystem>`
     - A virtualOverlay 2 filesystem implementation.
   * - :class:`QnxFs <dissect.target.filesystems.qnxfs.QnxFilesystem>`
     - No documentation
   * - :class:`SMB <dissect.target.filesystems.smb.SmbFilesystem>`
     - Filesystem implementation for SMB.
   * - :class:`SquashFS <dissect.target.filesystems.squashfs.SquashFSFilesystem>`
     - No documentation
   * - :class:`Virtual Backup Files <dissect.target.filesystems.vbk.VbkFilesystem>`
     - Filesystem implementation for VBK files.
   * - :class:`VMFS <dissect.target.filesystems.vmfs.VmfsFilesystem>`
     - No documentation
   * - :class:`XFS <dissect.target.filesystems.xfs.XfsFilesystem>`
     - No documentation

Operating Systems
~~~~~~~~~~~~~~~~~

Inside Dissect we have a variety of ``OSPlugins`` that it can infer from the data available on a target. Dissect detects these on the disks so it knows what kind of system it is trying to talk to. This way it can more accuratly query the users on a windows system for example.

The variety of the Operating Systems it can detect are as follows

.. list-table:: Supported Operating Systems
   :header-rows: 1
   :widths: 15 35

   * - Operating System
     - Description
   * - :class:`Android <dissect.target.plugins.os.unix.linux.android._os.AndroidPlugin>`
     - No documentation
   * - :class:`Bsd <dissect.target.plugins.os.unix.bsd._os.BsdPlugin>`
     - No documentation
   * - :class:`Citrix <dissect.target.plugins.os.unix.bsd.citrix._os.CitrixPlugin>`
     - No documentation
   * - :class:`Darwin <dissect.target.plugins.os.unix.bsd.darwin._os.DarwinPlugin>`
     - Darwin plugin.
   * - :class:`Debian <dissect.target.plugins.os.unix.linux.debian._os.DebianPlugin>`
     - No documentation
   * - :class:`ESXi <dissect.target.plugins.os.unix.esxi._os.ESXiPlugin>`
     - ESXi OS plugin
   * - :class:`Fortinet <dissect.target.plugins.os.unix.linux.fortios._os.FortiOSPlugin>`
     - FortiOS plugin for various Fortinet appliances.
   * - :class:`FreeBSD <dissect.target.plugins.os.unix.bsd.freebsd._os.FreeBsdPlugin>`
     - No documentation
   * - :class:`iOS <dissect.target.plugins.os.unix.bsd.darwin.ios._os.IOSPlugin>`
     - Apple iOS plugin.
   * - :class:`Generic Linux <dissect.target.plugins.os.unix.linux._os.LinuxPlugin>`
     - Linux plugin.
   * - :class:`MacOS <dissect.target.plugins.os.unix.bsd.darwin.macos._os.MacOSPlugin>`
     - No documentation
   * - :class:`OpenBSD <dissect.target.plugins.os.unix.bsd.openbsd._os.OpenBsdPlugin>`
     - No documentation
   * - :class:`dissect.target.loaders.profile.ProfileOSPlugin`
     - No documentation
   * - :class:`Proxmox <dissect.target.plugins.os.unix.linux.debian.proxmox._os.ProxmoxPlugin>`
     - No documentation
   * - :class:`RedHat <dissect.target.plugins.os.unix.linux.redhat._os.RedHatPlugin>`
     - "RedHat, CentOS and Fedora Plugin."
   * - :class:`dissect.target.loaders.res.ResOSPlugin`
     - No documentation
   * - :class:`OpenSusSE <dissect.target.plugins.os.unix.linux.suse._os.SuSEPlugin>`
     - No documentation
   * - :class:`Unix <dissect.target.plugins.os.unix._os.UnixPlugin>`
     - UNIX plugin.
   * - :class:`Vyos <dissect.target.plugins.os.unix.linux.debian.vyos._os.VyosPlugin>`
     - No documentation
   * - :class:`Windows <dissect.target.plugins.os.windows._os.WindowsPlugin>`
     - No documentation

Child Targets
~~~~~~~~~~~~~

Also known as targets within targets. These are, for example, virtual machines inside another virtual machine.
Dissect has the ability to find these Child targets using configuration files on the host itself.

These can be queried recursively, so Dissect can automatically find all targets within targets.
This holds true even if there is a target within those targets.

.. seealso::

    See :ref:`Child targets <advanced/targets:Targets in targets>` for more thorough explenation.

The Child targets we support and thus are able to automatically find are:

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
     - 
   * - :class:`Parallels <dissect.target.plugins.child.parallels.ParallelsChildTargetPlugin>`
     - Child target plugin that yields Parallels Desktop VM files.
   * - :class:`Podman <dissect.target.plugins.child.podman.PodmanChildTargetPlugin>`
     - 
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

