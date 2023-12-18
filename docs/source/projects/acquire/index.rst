acquire
=======

.. button-link:: https://github.com/fox-it/acquire
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

``acquire`` is a tool to quickly gather forensic artefacts from disk images or a live system into a lightweight container.
This makes ``acquire`` an excellent tool to, among others, speed up the process of digital forensic triage.
It uses Dissect to gather that information from the raw disk, if possible.

``acquire`` gathers artefacts based on modules. These modules are paths or globs on a filesystem which acquire attempts to gather.
Multiple modules can be executed at once, which have been collected together inside a profile.
These profiles (used with ``--profile``) are  ``full``, ``default``, ``minimal`` and ``none``.
Depending on what operating system gets detected, different artefacts are collected.

Installation
------------

``acquire`` is available on `PyPI <https://pypi.org/project/acquire/>`_.

.. code-block:: console

    $ pip install acquire

Usage
-----

The most basic usage of ``acquire`` is as follows:

.. code-block:: console

    $ sudo acquire

The tool requires administrative access to read raw disk data instead of using the operating system for file access.
However, there are some options available to use the operating system as a fallback option. (e.g ``--fallback`` or ``--force-fallback``)

Reference
---------

For more information regarding the usage of `acquire`, please refer to the :doc:`/tools/acquire` tool documentation.
