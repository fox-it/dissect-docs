target-dump
===========

With ``target-dump`` you can export records of a specific ``function`` used in target-query to a file.

The basic structure of a ``target-dump`` command is as follows:

.. code-block:: console

    $ target-dump -f <comma_seperated_functions> <path_to_target>

Furthermore, the tool can apply certain compression algorithms to the dump, to create small archives of the output.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.dump.run
    :func: main
    :prog: target-dump
    :hook:
