dissect.eventlog
================

.. button-link:: https://github.com/fox-it/dissect.eventlog
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing parsers for the Windows EVT, EVTX and WEVT log file formats.

Installation
------------

``dissect.eventlog`` is available on `PyPI <https://pypi.org/project/dissect.eventlog/>`_.

.. code-block:: console

    $ pip install dissect.eventlog

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to print all records in an
``.evtx`` or ``.evt`` file:

.. code-block:: python

    from dissect.eventlog.evtx import Evtx

    with open("/path/to/file.evtx", "rb") as fh:
        logfile = Evtx(fh)
        for record in logfile:
            print(record)

    with open("/path/to/file.evt", "rb") as fh:
        logfile = Evt(fh)
        for record in logfile:
            print(record)

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.eventlog`.
