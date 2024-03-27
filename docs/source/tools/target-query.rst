target-query
============

``target-query`` is a tool used to query specific data inside a one or more targets. These queries are available
in the form of ``functions`` that reside within :doc:`plugins </advanced/plugins>`. Each plugin is focussed on
providing specific functionality.

This functionality can range from parsing log sources, such as command history logs (i.e. bash history,
PowerShell history, etc.), to returning the hostname and operating system version.

The most basic usage of ``target-query`` is to execute a function on a target:

.. code-block:: console

    $ target-query -f <FUNCTION_NAME> /example_path/target.vmdk

You can also use basic path expansion to execute functions over multiple targets. For example, to execute a function
on all ``.vmdk`` files in a directory:

.. code-block:: console

    $ target-query -f <FUNCTION_NAME> /example_path/*.vmdk

.. seealso::

    Please refer to :doc:`/usage/use-cases` for more examples of how to use ``target-query``.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.query
    :func: main
    :prog: target-query
    :hook:

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.

The ``-f``, ``--function`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since ``target-query`` is based on functions, the ``-f``, ``--function`` argument is required. Its usage is
simple, supply the argument followed by the function(s) that you wish to run on the target(s).
So if you wish to run the ``runkeys`` function, it would look something like this:

.. code-block:: console

    $ target-query -f runkeys targets/EXAMPLE.tar
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2021-02-08 15:33:17.949652+00:00 name='SecurityHealth' path='%windir%/system32/SecurityHealthSystray.exe' key='HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='sysvol/windows/system32/config/SOFTWARE' username=None user_sid=None user_home=None>
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2021-02-08 15:33:17.949652+00:00 name='VMware VM3DService Process' path='"C:/Windows/system32/vm3dservice.exe" -u' key='HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='sysvol/windows/system32/config/SOFTWARE' username=None user_sid=None user_home=None>
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2021-02-08 15:33:17.949652+00:00 name='VMware User Process' path='"C:/Program Files/VMware/VMware Tools/vmtoolsd.exe" -n vmusr' key='HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='sysvol/windows/system32/config/SOFTWARE' username=None user_sid=None user_home=None>
    <windows/registry/run hostname='EXAMPLE' domain='EXAMPLE.local' ts=2021-12-09 12:06:20.037806+00:00 name='OneDriveSetup' path='C:/Windows/SysWOW64/OneDriveSetup.exe /thfirstsetup' key='HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' hive_filepath='C:\\Windows/ServiceProfiles/LocalService/ntuser.dat' username='LocalService' user_sid='S-1-5-19' user_home='%systemroot%\\ServiceProfiles\\LocalService'>

You can also execute multiple functions at the same time by separating each function name with a comma (``,``). For example ``-f hostname,version``.
Functions can have one of the following different output types:

* Records (please refer to :doc:`/tools/rdump` and :ref:`records <overview/index:records>`)
* Lines
* Text

This also means that functions with different output types cannot be run to together.

To list all available plugin functions and their description you can use the ``target-query --list`` argument to get an overview.
More detailed information on a specific plugin's function can be obtained using ``target-query -f [FUNCTION_NAME] -h``.

The ``--child`` argument
^^^^^^^^^^^^^^^^^^^^^^^^

The ``--child`` argument can be used to query a specific child within a target, for example when dealing with a
hypervisor. Provide either the full path to the child or the index of the child (where 0 is the first entry).

.. seealso::

    Please refer to :ref:`advanced/targets:targets in targets` for more information.

The ``--children`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a target contains multiple other targets, such as a hypervisor, the ``children`` argument includes all children for
the query as well.

.. seealso::

    Please refer to :ref:`advanced/targets:targets in targets` for more information.

The ``-l``, ``--list`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-l``, ``--list`` argument lists all the available functions and their short description. To get a more elaborate
description of a specific function, use ``target-query -f [FUNCTION_NAME] -h``.

The ``-s``, ``--strings`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-s``, ``--string`` argument prints the records as strings. This might come in handy when, for example,
post-processing the results with ``grep`` or other text-based tools.

The ``-j``, ``--json`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the output of a function is ``records``, the ``-j``, ``--json`` argument converts these ``records`` into JSON
format. This might come in handy when post-processing the results with a tool such as
`jq <https://stedolan.github.io/jq/>`_.

The ``--limit`` argument
^^^^^^^^^^^^^^^^^^^^^^^^

the ``--limit [LIMIT]`` limits the amount of returned records to the specified amount.

The ``--no-cache``, ``--ignore-cache`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To improve performance on repetitive queries, ``target-query`` can create cache files. The
``--no-cache``, ``--ignore-cache`` argument prevents ``target-query`` from creating these cache files.

.. seealso::

    Please refer to :ref:`advanced/plugins:caching` to learn more about in ``target-query``.

The ``--only-read-cache`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``--only-read-cache`` argument when the cache files should only be read and not written.

.. seealso::

    Please refer to :ref:`advanced/plugins:caching` to learn more about in ``target-query``.

The ``--rewrite-cache`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``--rewrite-cache`` argument rewrites the cache files, such that previous tracked progression is overwritten.

.. seealso::

    Please refer to :ref:`advanced/plugins:caching` to learn more about caching in ``target-query``.

The ``--cmdb`` argument
^^^^^^^^^^^^^^^^^^^^^^^

The ``--cmdb`` argument can be used to generate a CMDB output for the targets. This argument only works with basic OS
functions, namely ``hostname``, ``version``, ``domain``, ``ips``, and ``os``. The following example shows how it can be used:

.. code-block:: console

    $ target-query targets/* -f hostname,domain,version,ips --cmdb -d ";"
    EXAMPLE.vmx;EXAMPLE;EXAMPLE.local;Windows Server 2012 Enterprise (NT 6.3) 14393;["some.ip.address.here", "another.ip.address.here"]
    EXAMPLE.vmx;EXAMPLE;EXAMPLE.local;Windows Server 2016 Enterprise (NT 6.3) 14393;["some.ip.address.here", "another.ip.address.here"]
    EXAMPLE.tar;EXAMPLE;EXAMPLE.local;Red Hat Enterprise Linux 9.0;["some.ip.address.here", "another.ip.address.here"]

The ``--hash`` argument
^^^^^^^^^^^^^^^^^^^^^^^

The ``--hash`` argument hashes all the files located at the uri paths in the records, if the uri path can be resolved.
This can be useful to, for example, compare file hashes with known-good-hashes.

The ``--report-dir`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``--report-dir`` argument when you want to write the query result report to a specific location.

Loading separate files instead of targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To query separate (log) files instead of a target use the log:// uri.
Currently only the evt/evtx plugins support this feature.

.. code-block:: console

    $ target-query log:///path/to/evtxs/* -f evtx

