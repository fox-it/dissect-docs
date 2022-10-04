target-dd
=========

With ``target-dd`` you can export (a part of) a target to a file or to ``stdout``. At the moment, ``target-dd``
can be used for targets that have only one disk.

Usage
-----

.. sphinx_argparse_cli::
    :module: dissect.target.tools.dd
    :func: main
    :prog: target-dd
    :hook:

For more information on the ``-K``, ``--keychain-file`` and ``-Kv``, ``--keychain-value`` arguments, please refer to
:doc:`/usage/disk-encryption`.
