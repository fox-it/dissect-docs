dissect.cim
===========

.. button-link:: https://github.com/fox-it/dissect.cim
    :color: primary
    :outline:

    :octicon:`mark-github` View on GitHub

A Dissect module implementing a parser for the Windows Common Information Model (CIM) database, used in the Windows
operating system.

Installation
------------

``dissect.cim`` is available on `PyPI <https://pypi.org/project/dissect.cim/>`_.

.. code-block:: console

    $ pip install dissect.cim

This module is also automatically installed if you install the ``dissect`` package.

Usage
-----

This package is a library with no CLI tools, so you can only interact with it from Python. For example, to list all
``__FilterToConsumerBinding`` values:

.. code-block:: python

    from pathlib import Path
    from dissect.cim import CIM

    index = Path("/path/to/INDEX.BTR")
    objects = Path("/path/to/OBJECTS.DATA")
    mappings = [Path(f"/path/to/MAPPING{i}.map") for i in range(1, 4)]

    # CIM takes file-like objects of the INDEX.BTR, OBJECTS.DATA and MAPPING*.MAP files
    repo = CIM(index.open("rb"), objects.open("rb"), [m.open("rb") for m in mappings])

    subscription_ns = repo.root.namespace("subscription")
    try:
        for binding in subscription_ns.class_("__filtertoconsumerbinding").instances:
            consumer = subscription_ns.query(binding.properties["Consumer"].value)
            print("Query", consumer.properties["CommandLineTemplate"].value)
    except Exception:
        pass

Reference
---------

For more details, please refer to the API documentation of :mod:`dissect.cim`.
