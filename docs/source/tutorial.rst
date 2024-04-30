Tutorial
--------

For this tutorial we are going to use a well known case file from `NIST <https://cfreds.nist.gov/all/NIST/HackingCase>`_.
In this tutorial we assume Linux is used, on other operating systems most steps are the same but details may differ.
First of all, we install Python and create a venv:

.. code-block:: console

    $ python3 -m venv dissect

Now activate the virtual environment to get some work done:


.. code-block:: console

    $ source dissect/bin/activate
    

Let's download the case files. At the time of writing they are hosted at nist.gov.
On Linux:

.. code-block:: console

    $ for i in {1..8}; do curl https://cfreds-archive.nist.gov/images/hacking-dd/SCHARDT.00$i -o SCHARDT.00$i; done
    
.. note ::

    You can also download them manually of course.
    
Now, we are going to do some basic operations on this image. If you like, you can merge them together first,
although this is not strictly necessary:

.. code-block:: console

    $ for i in `ls SCHARDT.00*`; do cat $i >> SCHARDT.img; done


To get a brief summary of the forensic image, we use :doc:`target-info <tools/target-info>` like this:

.. code-block:: console

    $ target-info SCHARDT.img

The result will be something like this:

.. code-block:: console

    Disks
    - <Disk type="RawContainer" size="4871301120">

    Volumes
    - <Volume name="part_00007e00" size="4869333504" fs="NtfsFilesystem">

    Hostname       : N-1A9ODN6ZXK4LQ
    Domain         : None
    Ips            : 192.168.1.111
    Os family      : windows
    Os version     : Microsoft Windows XP (NT 5.1) 2600
    Architecture   : x86_32-win32
    Language       : 
    Timezone       : America/Chicago
    Install date   : 2004-08-19 22:48:27+00:00
    Last activity  : 2004-08-27 15:46:33.820240+00:00

To get the list of user accounts on this machine we use :doc:`target-query <target-query>`.
Another tool at our disposal is :doc:`rdump <rdump>`. By default target-query gives us records,
to process, filter and format results we can feed them to rdump, here we only select the name of the user:

.. code-block:: console

    $ target-query SCHARDT.img -f users | rdump -F name -C

The output is:

.. code-block:: console

    name
    systemprofile
    LocalService
    NetworkService
    Mr. Evil


To see what else we can query in this image, use the ``-l`` option:

.. code-block:: console

    $ target-query SCHARDT.img -l -q

.. note ::

    We also add ``-q`` to suppress warnings from plugins telling us they
    are not compatible with this forensic image.

You now see a list of plugins that you can use with the ``-f`` option.
Try a couple of them.

If we want to query for suspicious programs that might have been installed
on this machine we use the following command to generate a spreadsheet with
all binary files:

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs | rdump -s "r.path.suffix=='.exe'" -F path,ctime,mtime,size -C > db.csv

Here we use the ``-s`` option for rdump to filter on a particular file extension.
We use a *python expression* here (you can use any Python expression you like).
For more details see :doc:`rdump <rdump>`.

Finally, to inspect the system as if you were logged into it via a shell, invoke:

.. code-block:: console

    $ target-shell SCHARDT.img
    
Using :doc:`target-shell <target-shell>`, you can now navigate inside the target image by using the regular UNIX commands like
``ls``, ``cd``, ``find``, ``stat`` and so on.

This was just a quick introduction to the basic tools that are at your disposal.
To get an understanding of the basics of Dissect see:

* :doc:`target-query <target-query>`
* :doc:`target-shell <target-shell>`
* :doc:`acquire <acquire>`
* :doc:`rdump <rdump>`
