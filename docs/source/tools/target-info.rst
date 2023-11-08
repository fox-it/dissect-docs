target-info
===========

``target-info`` enables you to quickly view basic system information of your targets.

The following output types are supported:

- Human readable format (default)
- Record output (``-r``)
- JSON output (``-j`` and ``-J``)

The command below demonstrates ``target-info`` output on an :doc:`/tools/acquire` file.

.. code-block:: console

    $ target-info target.tar

    <Target target.tar>

    Hostname       : DC01
    Domain         : domain.local
    Ips            : 10.13.37.1
    Os family      : windows
    Os version     : Windows Server 2016 Datacenter (NT 10.0) 12345.6789
    Architecture   : amd64-win64
    Language       : en_US
    Timezone       : Europe/Berlin
    Install date   : 2020-04-29 10:48:49+00:00
    Last activity  : 2023-01-02 13:37:00+00:00

The command below demonstrates ``target-info`` output in JSON format using the option ``-j``. Use the option ``-J`` to generate JSON line output.

.. code-block:: console

    $ target-info -j target.vmx
.. code-block:: json

    {
        "disks": [
            {"type": "VmdkContainer", "size": 21474836480}
        ],
        "volumes": [
            {"name": "part_00100000", "size": 1048064, "fs": "NoneType"},
            {"name": "part_00200000", "size": 1902116352, "fs": "ExtFilesystem"},
            {"name": "part_71800000", "size": 19569573376, "fs": "NoneType"},
            {"name": "ubuntu--vg-ubuntu--lv", "size": 10737418240, "fs": "ExtFilesystem"}
        ],
        "children": [],
        "hostname": "SERVER01",
        "domain": "domain.local",
        "ips": ["10.13.37.2"],
        "os_family": "linux",
        "os_version": "Ubuntu 22.04.1 LTS",
        "architecture": "x86_64-linux",
        "language": ["en_US"],
        "timezone": "Etc/UTC",
        "install_date": "2023-02-02 12:07:32.646006+00:00",
        "last_activity": "2023-10-16 15:06:34.472182+00:00"
    }

The command below demonstrates ``target-info`` output using the option ``-r`` in :ref:`record <overview/index:records>` format.

.. code-block:: console
    :class: pre-wrap

    $ target-info -r target.vmx

    <target/info hostname='DESKTOP01' domain='DOMAIN' last_activity=2023-10-16 14:06:33.678421+00:00 install_date=2023-02-01 15:01:07+00:00 ips=[net.ipaddress('10.13.37.3')] os_family='windows' os_version='Windows 10 Pro (NT 10.0) 19045.2006' architecture='amd64-win64' language=['en_GB', 'en_US'] timezone='Europe/Berlin' disks=["{'type': 'VmdkContainer', 'size': 34359738368}"] volumes=["{'name': 'EFI system partition', 'size': 209714688, 'fs': 'FatFilesystem'}", "{'name': 'Microsoft reserved partition', 'size': 134217216, 'fs': 'NoneType'}", "{'name': 'Basic data partition', 'size': 34013707776, 'fs': 'NtfsFilesystem'}"] children=["{'type': 'wsl', 'path': 'C:\\\\Users\\\\user\\\\AppData\\\\Local\\\\Packages\\\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\\\LocalState\\\\ext4.vhdx'}"]>

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.info
    :func: main
    :prog: target-info
    :hook:
