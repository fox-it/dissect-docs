Tutorial
--------
### Let's get started!
For this tutorial we are going to use a well known case file from `NIST <https://cfreds.nist.gov/all/NIST/HackingCase>`_.
In this tutorial we assume Linux is used, on other operating systems most steps are the same but details may differ.
First of all, we install Python and create a venv:

.. code-block:: console

    $ python3 -m venv dissect

.. note ::

    Learn how to :doc:`install Dissect </install>`

Now activate the virtual environment to get some work done:


.. code-block:: console

    $ source dissect/bin/activate
    

Let's download the case files. At the time of writing they are hosted at nist.gov.
On Linux:

.. code-block:: console

    $ for i in {1..8}; do curl https://cfreds-archive.nist.gov/images/hacking-dd/SCHARDT.00$i -o SCHARDT.00$i; done
    
.. note ::

    You can also download them manually of course.
   ###  Basic operations
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

To get the list of user accounts on this machine we use two tools :doc:`target-query <target-query>` and :doc:`rdump <rdump>`. `target-query`, as the names suggests, allows to query the images and produces records by default. `rdump` is used to process, filter and format the query results. Here we only select the name of the user:

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
on this machine, one option could be to search for all the files with an ``.exe``
extension and then try to identify a malicious one. To this end, our first step is to use the
``walkfs`` plugin, that yields all files in the image:

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs
    
    <filesystem/entry path='\sysvol\...\Local Settings' size=0 ...>
    <filesystem/entry path='\sysvol\...\desktop.ini' size=62.0 ...>
    
This command returns a huge list of files. Our next step is to narrow this
list down to only files ending with ``.exe``. To accomplish this, we will again use ``rdump``, the same filtering tool mentioned in the previous command, and apply a
Python expression for filtering:

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs | rdump -s "r.path.suffix=='.exe'"
    
    <filesystem/entry path='\sysvol\...\winfo.exe' size=811.0 ...>
    <filesystem/entry path='\sysvol\...\pwdump.exe' size=1162.0 ...>


Here we use the ``-s`` option for rdump to filter on a particular file extension.
The expression ``r.path.suffix=='.exe'`` is a snippet of Python that examines
the suffix of each path and only includes the ones ending with ``.exe``.
You can use any Python expression you like!

While this list is much better, we can still improve the formatting.
We use the ``-F`` option from ``rdump`` to filter the columns:

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs | rdump -s "r.path.suffix=='.exe'" -F path,ctime,mtime,size
    
This reduces the number of characters per line significantly.
However due to the record representation, it is still hard to read
(hence no output example is shown)
To make it even more readable, we add the
``-C`` option which converts it to a comma separated format:

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs | rdump -s "r.path.suffix=='.exe'" -F path,ctime,mtime,size -C
    
    \sysvol\winfo.exe,2004-08-19 22:25:09.860123+00:00,2004-08-19 23:05:15.852375+00:00,41.6 KB
    \sysvol\pwdump.exe,2004-08-19 22:25:09.860123+00:00,2004-08-19 23:05:15.852375+00:00,41.6 KB
    \sysvol\...\LookAtLan.exe,2004-08-19 22:25:09.860123+00:00,2004-08-19 23:05:15.852375+00:00,41.6 KB


This already looks much more compact and searchable. Finally, we can put the resulting table
in a spreadsheet for further investigation. We accomplish this by simply adding ``> db.csv``

.. code-block:: console

    $ target-query SCHARDT.img -f walkfs | rdump -s "r.path.suffix=='.exe'" -F path,ctime,mtime,size -C > db.csv

You can now open the ``db.csv`` file in your favourite spreadsheet program and
search for well known malicious executables.


In our database we find a program that can be
used for hacking: LookAtLan.exe. We can open a shell to the image to further investigate the
compromised system and locate the hacking program:

.. code-block:: console

    $ target-shell SCHARDT.img
    
Using :doc:`target-shell <target-shell>`, you can now navigate inside the target image by using the regular UNIX commands like
``ls``, ``cd``, ``find``, ``stat`` and so on.

So we can navigate to one of the suspicious files we found like this:

.. code-block:: console

    N-1A9ODN6ZXK4LQ /> cd C:\Program Files\Look@LAN\
    N-1A9ODN6ZXK4LQ /C:/Program Files/Look@LAN> ls
    ...
    LookAtLan.exe
    ...


This was just a quick introduction to the basic tools that are at your disposal.
To get an understanding of the basics of Dissect see:

* :doc:`acquire <acquire>`
* :doc:`rdump <rdump>`
* :doc:`target-mount <target-mount>`
* :doc:`target-query <target-query>`
* :doc:`target-shell <target-shell>`

