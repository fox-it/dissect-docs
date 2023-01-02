Use-cases
=========

The use-cases presented here can be used as a source of inspiration and as a quick reference on how to tackle specific 
challenges you might encounter during your investigations. 

.. note:: 

    Consider this page as a constant WIP. This page will continuously be updated with new use-cases as we or the community document them.

    We also appreciate your help! If you have a new use-case, feel free to contact us or create a pull request on `GitHub <https://github.com/fox-it/dissect-docs>`_.

Finally, for the use-cases written out below the environment as described in :doc:`/usage/first-steps/index` is assumed.


target-query
------------

Creating a simple CMDB
~~~~~~~~~~~~~~~~~~~~~~

As explained in :doc:`/tools/target-query`, you can create a CMDB using ``target-query``. Simply use the ``--cmdb``
argument, while using the basic OS functions. You can write this to a csv file to archive your CMDB.

.. code-block:: console

    $ target-query targets/* -f hostname,domain,OS,version,ips --cmdb -d ";" > docs/CMDB.csv

Pushing query results to a search platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's parse all the Windows event logs using the ``evt`` and the ``evtx`` function and get them in a JSON format.
Since both functions output their results as records, we can use :doc:`/tools/rdump` to obtain a prettified JSON output
with the ``-j`` argument, or a more compact JSON output with ``-J``.

.. code-block:: console

    $ target-query targets/ -f evt,evtx -q | rdump -j
    [...]
    {
        "hostname": "N-1A9ODN6ZXK4LQ",
        "domain": null,
        "ts": "2004-08-19T22:20:40.000000",
        "TimeGenerated": "2004-08-19T22:20:40.000000",
        "TimeWritten": "2004-08-19T22:20:40.000000",
        "SourceName": "LoadPerf",
        "EventID": 1073742824,
        "EventCode": 1000,
        "EventFacility": 0,
        "EventCustomerFlag": 0,
        "EventSeverity": 1073741824,
        "EventType": 4,
        "EventCategory": 0,
        "Computername": "N-1A9ODN6ZXK4LQ",
        "UserSid": null,
        "Strings": [
            "RSVP",
            "QoS RSVP"
        ],
        "Data": "DBQAAA==",
        "_source": "/home/dev/Documents/hacking_case/4Dell Latitude CPi.E01",
        "_classification": null,
        "_generated": "2022-07-13T11:42:20.621391",
        "_version": 1,
        "_type": "record",
        "_recorddescriptor": [
            "filesystem/windows/evt",
            3573162258
        ]
    }
    [...]

Note that the code block above gives an example of how this data comes through in the console and does not represent the
full output (indicated with ``[...]``).

In a lot of cases, you want to push this data to some sort of search platform. To demonstrate this functionality here,
we pipe the output to ``nc`` and stream it to ``localhost`` on port ``1337``.

.. code-block:: console

    $ target-query targets/ -f evt,evtx -q | rdump -j | nc localhost 1337

In another terminal we listen to any data coming in on port 1337, resulting in receiving the data in the same JSON
format.

.. code-block:: console

    $ nc -l 1337
    [...]
    {
        "hostname": "N-1A9ODN6ZXK4LQ",
        "domain": null,
        "ts": "2004-08-19T22:20:40.000000",
        "TimeGenerated": "2004-08-19T22:20:40.000000",
        "TimeWritten": "2004-08-19T22:20:40.000000",
        "SourceName": "LoadPerf",
        "EventID": 1073742824,
        "EventCode": 1000,
        "EventFacility": 0,
        "EventCustomerFlag": 0,
        "EventSeverity": 1073741824,
        "EventType": 4,
        "EventCategory": 0,
        "Computername": "N-1A9ODN6ZXK4LQ",
        "UserSid": null,
        "Strings": [
            "RSVP",
            "QoS RSVP"
        ],
        "Data": "DBQAAA==",
        "_source": "/home/dev/Documents/hacking_case/4Dell Latitude CPi.E01",
        "_classification": null,
        "_generated": "2022-07-13T11:42:20.621391",
        "_version": 1,
        "_type": "record",
        "_recorddescriptor": [
            "filesystem/windows/evt",
            3573162258
        ]
    }
    [...]

Luckily, you don't have to reinvent the wheel when pushing data to well-known search platforms, such as Splunk or
Elasticsearch. ``rdump`` can make use of its dedicated adapters for these search platforms.

Let's take a look at Splunk for example. For this, we use the ``-w`` argument for ``rdump`` and invoke the Splunk
adapter with ``splunk://localhost:1337``.

.. code-block:: console

    $ target-query targets/ -f evt,evtx -q | rdump -w splunk://localhost:1337

For demonstration purposes, we again listen in another terminal to port 1337 with ``nc`` to see the result coming in.

.. code-block:: console

    $ nc -l 1337
    [...]
    type="filesystem/windows/evt" rdtag=None hostname="N-1A9ODN6ZXK4LQ" domain=None ts="2004-08-19 22:20:40" TimeGenerated="2004-08-19 22:20:40" TimeWritten="2004-08-19 22:20:40" SourceName="LoadPerf" EventID="1073742824" EventCode="1000" EventFacility="0" EventCustomerFlag="0" EventSeverity="1073741824" EventType="4" EventCategory="0" Computername="N-1A9ODN6ZXK4LQ" UserSid=None Strings="['RSVP', 'QoS RSVP']" Data="DBQAAA=="
    [...]

As you can see, these results are Splunk compatible and will allow the records to be imported into your Splunk instance.

Timeline of records
~~~~~~~~~~~~~~~~~~~

``target-query`` functions that have a ``record`` with the fiedltype ``datetime`` are outputed in a single record. As shown below with the function ``mft``:

.. code-block:: console

    $ target-query -f mft -t targets/EXAMPLE.tar --limit 1 | rdump
    <filesystem/ntfs/mft/std hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411+00:00 last_modification_time=2019-03-19 21:52:25.169411+00:00 last_change_time=2019-03-19 21:52:25.169411+00:00 last_access_time=2019-03-19 21:52:25.169411+00:00 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>

Using ``rmulti-timestamp`` between ``target-query`` outputs multiple ``ts`` enriched records based on the ``datetime`` fields of the original record.

.. code-block:: console

    $ target-query -f mft -t targets/EXAMPLE.tar --limit 1 | rmulti-timestamp | rdump
    [reading from stdin]
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='creation_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_modification_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_change_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>
    <filesystem/ntfs/mft/std ts=2019-03-19 21:52:25.169411 ts_description='last_access_time' hostname='MSEDGEWIN10' domain=None creation_time=2019-03-19 21:52:25.169411 last_modification_time=2019-03-19 21:52:25.169411 last_change_time=2019-03-19 21:52:25.169411 last_access_time=2019-03-19 21:52:25.169411 segment=0 path='c:/$MFT' owner='S-1-5-18' filesize=0.12 GB resident=False inuse=True volume_uuid=None>

This makes it possible to output a timeline of records that can be analyzed in applications like Elasticsearch (``-w elastic://``), Timesketch (``--jsonlines``) or Timeline Explorer (``--csv``) using ``rdump``. These application need a single ``datetime`` field on which can be filtered to view records in chronological order.

Filtering function output using target-query and rdump
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using ``rdump`` it is also possible to filter the output you generate when using ``target-query``. Below you will find
two simple use-cases on how to filter output.

Using the ``rdump`` filter defined below, you can filter the output from the ``mft`` function to just show the malicious
``random_01.dll`` dll.

.. code-block:: console

    $ target-query -f mft targets/MSEDGEWIN10.tar | rdump -s 'r.path.filename == "random_01.dll"'
    <filesystem/ntfs/mft/std hostname='MSEDGEWIN10' domain=None creation_time=2021-02-09 07:36:23.757454 last_modification_time=2021-01-22 10:01:00 last_change_time=2021-02-08 17:42:46.283194 last_access_time=2021-02-09 07:36:23.771214 segment=918 path='c:/Users/Default/Downloads/random_01.dll' owner='S-1-5-32-544' filesize=3.28 MB resident=False inuse=True volume_uuid='3fa6fe91-916a-4c89-ab18-cd58de1c8fab'>
    <filesystem/ntfs/mft/filename hostname='MSEDGEWIN10' domain=None creation_time=2021-02-09 07:36:23.757454 last_modification_time=2021-02-09 07:36:23.757454 last_change_time=2021-02-09 07:36:23.757454 last_access_time=2021-02-09 07:36:23.757454 filename_index=1 segment=918 path='c:/Users/Default/Downloads/random_01.dll' owner='S-1-5-32-544' filesize=3.28 MB resident=False inuse=True ads=False volume_uuid='3fa6fe91-916a-4c89-ab18-cd58de1c8fab'>

You can filter the output of other functions like ``evtx`` as well. By combining multiple filters we can filter on
remote interactive login events, namely ``EventID == 4624`` and ``LogonType == "10"``. Then we format the data how we
want and sort it to get a chronological overview of remote interactive logins!

.. code-block:: console

    $ target-query targets/MSEDGEWIN10.tar -f evtx | rdump -s 'r.EventID == 4624 and r.LogonType == "10"' -f '{ts} - {TargetUserSid} {TargetDomainName}\\{TargetUserName}' | sort
    [...]
    2021-06-02 - 13:37:26.628687 S-1-5-21-418967180-7773086473-4073416957-500 MSEDGEWIN10\\Administrator
    [...]

It is possible to create even more elaborate filters using ``rdump``. For a complete overview please refer to the
:doc:`/tools/rdump` documentation.

target-fs
---------

Hashing a file using target-fs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hashing a file from a target using target-fs is pretty simple. All you have to do is supply the ``target``, the ``cat``
sub-command and the path to the file within the target. The binary contents will now be printed to ``stdout``. 
By piping it to ``sha256sum`` you can create a checksum for easy comparison or check it in your hash database of choice. 


.. code-block:: console

    $ target-fs targets/MSEDGEWIN10.tar cat "C:\Windows\System32\Drivers\null.sys" | sha256sum
    32c714dd5588e5cdacc6980044d2a66a28c42b0d5208ac2ffbac5d64be95568  -


target-reg
----------

Listing subkeys of a specific registry key and outputing their contents using ``target-reg``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listing the available subkeys of a specific registry key pretty easy using ``target-reg``. You can do so by following the example below. 

.. code-block:: console 

    $ target-reg targets/MSEDGEWIN10.tar -k "HKLM\\SYSTEM\\CURRENTCONTROLSET\\ENUM\\USB\\VID_0E0F&PID_0003&MI_00"
    + 'VID_0E0F&PID_0003&MI_00' (2020-12-09 12:06:15.867247+00:00)
      + '7&3ae26960&0&0000' (2022-08-17 10:56:49.798122+00:00)
          - 'DeviceDesc' '@input.inf,%hid.devicedesc%;USB Input Device'
          - 'LocationInformation' '000b.0000.0000.005.000.000.000.000.000'
          - 'Capabilities' 128
          - 'Address' 5
          - 'ContainerID' '{ee33e11a-3a16-11eb-bde6-806e6f6e6963}'
          - 'HardwareID' ['USB\\VID_0E0F&PID_0003&REV_0102&MI_00', 'USB\\VID_0E0F&PID_0003&MI_00']
          - 'CompatibleIDs' ['USB\\Class_03&SubClass_00&Prot_00', 'USB\\Class_03&SubClass_00', 'USB\\Class_03']
          - 'ClassGUID' '{745a17a0-74d3-11d0-b6fe-00a0c90f57da}'
          - 'Service' 'HidUsb'
          - 'Driver' '{745a17a0-74d3-11d0-b6fe-00a0c90f57da}\\0000'
          - 'Mfg' '@input.inf,%stdmfg%;(Standard system devices)'
          - 'ConfigFlags' 0
          - 'ParentIdPrefix' '8&367bfb7c&0'

Note that the ``+`` in the output above indicates a registry key and the ``-`` indicates a registry value.

Knowing this, we can output the contents of the key value ``ClassGUID``, under the registry key ``7&3ae26960&0&0000`` 
to ``stdout`` by using the following command:

.. code-block:: console

    $ target-reg targets/MSEDGEWIN10.tar -k "HKLM\\SYSTEM\\CURRENTCONTROLSET\\ENUM\\USB\\VID_0E0F&PID_0003&MI_00\\7&3ae26960&0&0000" -kv "ClassGUID"
    <RegfValue Driver='{745a17a0-74d3-11d0-b6fe-00a0c90f57da}\\0000'>


