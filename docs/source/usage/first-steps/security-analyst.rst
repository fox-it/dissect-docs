Next steps as a Security Analyst
================================

.. note::

    This page assumes you're already familiar with basic analysis steps as outlined in :doc:`/usage/first-steps/incident-handler`.

Now that triage has been performed, we can deep dive a bit more into the capabilities of Dissect. This is
where the work of a Security Analyst comes into play. Please note that what is shown in this section, is only a small
subset of the capabilities; it's meant to be used as a source of inspiration!

Performing IOC checks on multiple targets using ``target-fs``
-------------------------------------------------------------

Let's take a look at how ``target-fs`` can be of use during an investigation. Even though the ``ls`` sub-command does a
very simple thing (listing a directory), combining it with other tools like ``find``, ``grep``, and ``xargs`` can make
it quite powerful.

Say, you want to look for an IOC in the form of a known malicious file named ``null.sys`` which is located in the
``C:\Windows\System32\Drivers\`` directory. With ``find``, you can go recursively through the
``targets/`` directory to list all the available targets. Next, pipe the results of ``find`` to
``xargs`` to use the found targets for ``target-fs`` with the use of ``sh``. Use the ``ls`` sub-command to list all the
files within the ``C:\Windows\System32\Drivers\`` directory and use ``grep`` to filter the driver files per target for
the file ``null.sys``. The example below shows how this all comes together.

.. code-block:: console

    $ find targets/ -type f -print0 | sort -z | xargs -r0I {} sh -c 'echo "[+] checking $(basename "{}")"; target-fs "{}" -q ls C:\\Windows\\System32\\Drivers\\ | grep -iF null.sys'
    [+] checking 4Dell Latitude CPi.E01
    null.sys
    [+] checking IE11-Win81-VMWare-disk1.vmdk
    null.sys
    [+] checking MSEDGEWIN10.tar
    null.sys
    [+] checking SCHARDT.001
    null.sys

The console output reveals that all targets contain the ``null.sys`` file. This makes sense, since ``null.sys`` is not a
malicious file, it is a driver which is present on a Windows system by default.

Hashing multiple files on multiple targets using ``target-fs``
--------------------------------------------------------------

The ``cat`` sub-command for ``target-fs`` can be used in combination with ``sha256`` to quickly identify malicious files
or compare files based on their hash. The code block below shows how this is done for the ``null.sys`` file present on
target ``MSEDGEWIN10.tar``.

.. code-block:: console

    $ target-fs targets/MSEDGEWIN10.tar -q cat "C:\Windows\System32\Drivers\null.sys" | sha256sum
    732c714dd5588e5cdacc6980044d2a66a28c42b0d5208ac2ffbac5d64be95568  -

To expand this to check multiple files on multiple targets, you can reuse the logic from
:ref:`usage/first-steps/security-analyst:performing ioc checks on multiple targets using ``target-fs```. So again, use
``find`` and ``xargs`` to get all the available targets. Now use the logic in the above code block in combination with a
for-loop to get the MD5 hash of the ``null.sys`` as well as the ``ntfs.sys`` file.

.. code-block:: console

    $ find targets/ -type l -print0 | sort -z | xargs -r0I {} sh -c 'echo "[+] checking $(basename "{}")"; for i in "null.sys" "ntfs.sys"; do target-fs "{}" -q cat "C:\Windows\System32\Drivers\\${i}" | sha256sum | xargs -I [] echo $i - []; done'
    [+] checking 4Dell LattitudeCPi.E01
    null.sys - b21133a75253ec15e2dff66d3b480ab1a7e1a2360476c810e7aa55d0f0eb08d4  -
    ntfs.sys - 72d254452a783c750f9c41974f906defaf807db6d28276b0ff03ac20e783ee1b  -
    [+] checking IE11-Win81-VMWare-disk1.vmdk
    null.sys - dbc07bbc54ebc2d2e576b23a4ce116b3da988577ad0d96cb7289a6748a60f9ea  -
    ntfs.sys - 03acd858bb8388d263e99ee5ecc53d9fc9747869e01e821ab36ae53fdefac8f5  -
    [+] checking MSEDGEWIN10.tar
    null.sys - 732c714dd5588e5cdacc6980044d2a66a28c42b0d5208ac2ffbac5d64be95568  -
    ntfs.sys - d5d5aea846792a87bafcfcc3bc5fc57316b83a71269f3376a647d25c65368bec  -
    [+] checking SCHARDT.001
    null.sys - b21133a75253ec15e2dff66d3b480ab1a7e1a2360476c810e7aa55d0f0eb08d4  -
    ntfs.sys - 72d254452a783c750f9c41974f906defaf807db6d28276b0ff03ac20e783ee1b  -

Extract a (malicious) file from a target
----------------------------------------

With ``target-shell`` as well as ``target-fs``, we are able to extract files from almost any target. Above in
:ref:`usage/first-steps/security-analyst:hashing multiple files on multiple targets using ``target-fs``` we have looked
at the ``null.sys``. Let's retrieve this file from the target ``IE11-Win81-VMWare-disk1.vmdk`` and checksum it again to
see if we get the same result.

To do this, you first open a shell on the target as demonstrated in :doc:`/tools/target-shell`. When the shell is
obtained, you can use the ``find`` sub-command to retrieve the exact location of the ``null.sys`` driver.

.. code-block:: console

    $ target-shell IE11-Win81-VMWare-disk1.vmdk -q
    IE11WIN8_1 /> find -iname null.sys /
    /sysvol/Windows/System32/drivers/null.sys
    /sysvol/Windows/WinSxS/amd64_microsoft-windows-null_31bf3856ad364e35_6.3.9600.16384_none_9a244d87eef4113b/null.sys
    /c:/Windows/System32/drivers/null.sys
    /c:/Windows/WinSxS/amd64_microsoft-windows-null_31bf3856ad364e35_6.3.9600.16384_none_9a244d87eef4113b/null.sys

Perfect, we found the exact location of the file we are looking for, namely
``/sysvol/Windows/System32/drivers/null.sys``. Using the ``save`` sub-command, you can retrieve the file to your host
system to your preferred location with the ``-o`` argument.

.. code-block:: console

    $ target-shell IE11-Win81-VMWare-disk1.vmdk -q
    IE11WIN8_1 /> save /sysvol/Windows/System32/drivers/null.sys -o /home/user/export

Using ``sha256`` shows us that the file has been properly extracted to our preferred directory.

.. code-block:: console

    $ sha256sum /home/user/export
    dbc07bbc54ebc2d2e576b23a4ce116b3da988577ad0d96cb7289a6748a60f9ea  /home/user/export/null.sys

Finding hijacked CLSIDs
-----------------------

In some cases, malware can hijack CLSIDs to obtain persistence on a system. Let's assume that you found malware that is
somehow capable of changing the value of CLSID ``0000002F-0000-0000-C000-000000000046`` on target
``IE11-Win81-VMWare-disk1.vmdk``. For a normal functioning system, this CLSID has the value
``C:\Windows\System32\oleaut32.dll``, but the malware changes this to the location of a randomly named malicious
DLL.

To check if the other targets contain this malware, you can use the logic from
:ref:`usage/first-steps/security-analyst:performing ioc checks on multiple targets using ``target-fs```. This time, you
use ``target-query`` with the ``clsid`` function and use the ``-s`` (or ``--string``) argument in order to use ``grep``
on the results. With ``grep``, you first filter all CLSIDs for the one you're looking for, namely
``0000002F-0000-0000-C000-000000000046``. After this, you pipe the result to another ``grep`` were you look for those
results that do not contain the expected value, namely ``C:\Windows\System32\oleaut32.dll``. These hits will reveal the
targets that contain the modified CLSID as well.

.. code-block:: console

    $ find targets/ -type l -print0 | sort -z | xargs -r0I {} sh -c 'echo "[+] checking $(basename "{}")"; target-query "{}" -f clsid --string -q | grep 0000002F-0000-0000-C000-000000000046 | grep -ivF C:\\\\Windows\\\\System32\\\\oleaut32.dll'
    [+] checking 4Dell Latitude CPi.E01
    <windows/registry/clsid hostname='N-1A9ODN6ZXK4LQ' domain=None ts=2004-08-19 22:32:17.675291 clsid='{0000002F-0000-0000-C000-000000000046}' name='CLSID_RecordInfo' value='oleaut32.dll' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='$$$PROTO.HIV\\Classes\\CLSID\\{0000002F-0000-0000-C000-000000000046}\\InprocServer32' username=None user_id=None user_home=None>
    [+] checking IE11-Win81-VMWare-disk1.vmdk
    <windows/registry/clsid hostname='IE11WIN8_1' domain=None ts=2013-08-22 15:43:50.359442+00:00 clsid='{0000002F-0000-0000-C000-000000000046}' name='CLSID_RecordInfo' value='C:\\Users\\Default\\Downloads\\random_01.dll' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='CsiTool-CreateHive-{00000000-0000-0000-0000-000000000000}\\Classes\\CLSID\\{0000002F-0000-0000-C000-000000000046}\\InprocServer32' username=None user_id=None user_home=None>
    [+] checking MSEDGEWIN10.tar
    <windows/registry/clsid hostname='MSEDGEWIN10' domain=None ts=2019-03-19 21:54:26.107075+00:00 clsid='{0000002F-0000-0000-C000-000000000046}' name='CLSID_RecordInfo' value='C:\\Users\\Default\\random_02.dll' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='CsiTool-CreateHive-{00000000-0000-0000-0000-000000000000}\\Classes\\CLSID\\{0000002F-0000-0000-C000-000000000046}\\InprocServer32' username=None user_id=None user_home=None>
    [+] checking SCHARDT.001

Upon analysis, it shows here that the host ``MSEDGEWIN10`` is also infected with the malware. Host ``N-1A9ODN6ZXK4LQ``
is not, since it appears that in some case ``C:\Windows\\System32\`` is omitted for the value and that's why it shows up
in our ``grep`` results; a classic false positive.

Instead of using ``grep``, you can also use ``rdump`` to obtain the same results. We've seen its filtering options, so
let's use that to our advantage. By filtering on ``clsid == "{0000002F-0000-0000-C000-000000000046}"`` and on
``"oleaut32.dll" not in value`` we get the following result:

.. code-block:: console

    $ find targets/ -type f -print0 | sort -z | xargs -r0I {} sh -c "echo \"[+] checking $(basename \"{}\")\"; target-query \"{}\" -f clsid -q | rdump -s 'r.clsid == \"{0000002F-0000-0000-C000-000000000046}\" and \"oleaut32.dll\" not in r.value'"
    [+] checking ./4Dell Latitude CPi.E01
    [reading from stdin]
    [+] checking ./IE11-Win81-VMWare-disk1.vmdk
    [reading from stdin]
    <windows/registry/clsid hostname='IE11WIN8_1' domain=None ts=2013-08-22 15:43:50.359442+00:00 clsid='{0000002F-0000-0000-C000-000000000046}' name='CLSID_RecordInfo' value='C:\\Users\\Default\\Downloads\\random_01.dll' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='CsiTool-CreateHive-{00000000-0000-0000-0000-000000000000}\\Classes\\CLSID\\{0000002F-0000-0000-C000-000000000046}\\InprocServer32' username=None user_id=None user_home=None>
    [+] checking ./MSEDGEWIN10.tar
    [reading from stdin]
    <windows/registry/clsid hostname='MSEDGEWIN10' domain=None ts=2019-03-19 21:54:26.107075+00:00 clsid='{0000002F-0000-0000-C000-000000000046}' name='CLSID_RecordInfo' value='C:\\Users\\Default\\random_02.dll' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='CsiTool-CreateHive-{00000000-0000-0000-0000-000000000000}\\Classes\\CLSID\\{0000002F-0000-0000-C000-000000000046}\\InprocServer32' username=None user_id=None user_home=None>
    [+] checking ./SCHARDT.001
    [reading from stdin]

This gives us the same results as with our ``grep`` approach.
