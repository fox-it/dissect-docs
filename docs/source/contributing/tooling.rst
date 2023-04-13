Tooling
=======

Each project includes tooling for building and testing code and documentation.

The build system adheres to `PEP 517 <https://peps.python.org/pep-0517/>`_, `PEP 518 <https://peps.python.org/pep-0518/>`_
and `PEP 626 <https://peps.python.org/pep-0626>`_.
Together with ``tox``'s ``isolated_build`` feature this ensures that there are no hidden
dependencies on locally installed packages.

The ``tox.ini`` and ``pyproject.toml`` files will make sure the correct
versions of all build, test and install dependencies (including the version of ``tox`` itself) are present or are
installed during the build and test runs.

Building
~~~~~~~~

To build source and wheel distributions of a project, run ``tox`` with the ``build`` testenv:

.. code-block:: console

    $ tox -e build

The source and wheel distributions are put in the ``dist/`` directory in the root of the project. Building is done using
the default CPython 3 version on your system.

Testing
~~~~~~~

The default ``tox`` run will lint and unit test the code:

.. code-block:: console

    $ tox

Linting is done using flake8 and unit tests (if applicable) are run against the default installed CPython 3 and PyPy 3.
Make sure that the default Python version on your system is 3.9 if you want to run the unit tests using a supported
Python version.

To explicitly run the unit tests against a Python version use:

.. code-block:: console

    $ tox -e py310

Or in case of using PyPy:

.. code-block:: console

    $ tox -e pypy310

To run just the linting:

.. code-block:: console

    $ tox -e lint


If linting fails, you can try to automatically fix the linting using the following command:

.. code-block:: console

    $ tox -e fix

.. warning::
    Always check the results of ``tox -e fix`` before submitting as the proposed changes may not always be the most optimal solution.

Testing documentation
~~~~~~~~~~~~~~~~~~~~~

There is tooling to:

- generate the API documentation for manual inspection in a web browser
- automatically check for broken URLs in the documentation.


Previewing documentation
^^^^^^^^^^^^^^^^^^^^^^^^

You can generate the API documentation in HTML format using ``tox`` for viewing in a web browser as follows:

.. code-block:: console

    $ tox -e docsbuild

This will create the ``tests/docs/build/html`` directory with the generated documentation in HTML format.
Apart from the styling, this will show you how your documentation will appear
on https://docs.dissect.tools if your changes are accepted.


.. note::
    It is not unusual that warnings and errors appear while building; you can safely ignore them as long as the building of the documentation does not fail in its entirety.

After the build process has finished, you can view the documentation in, for example, Firefox:

.. code-block:: console

     $ firefox tests/docs/build/html/index.html


Checking external URLs
^^^^^^^^^^^^^^^^^^^^^^

If you include external website URLs in your API documentation, it is good to validate if these
links are still valid before commiting your changes.

You can check for broken links by invoking the following command:

.. code-block:: console

    $ tox -e docslinkcheck


You will see the results of the checks in your terminal, but they can also be found in the file
``tests/docs/build/linkcheck/output.txt``.

The following section helps you understand the results of the command.

Understanding linkcheck output
""""""""""""""""""""""""""""""

Each line in ``tests/docs/build/linkcheck/output.txt`` corresponds to one URL that has been checked and shows:
- the filename and line number where the URL is mentioned
- the result of the check
- the actual URL that was checked.

Use the following table to interpret the result of the check:

.. list-table:: How to process linkcheck results
   :widths: 20 40 40
   :header-rows: 1

   * - Result Code
     - Meaning
     - Resolve
   * - ok
     - The URL resolves without issues
     - No change required
   * - redirect
     - The URL resolves after following a redirect
     - No change required
   * - broken
     - The URL doesn't appear to be working.
     -
        - If the refererenced page has been moved, replace the URL with its new location
        - If the refererenced page is no longer available, consider creating an `archive.org <https://archive.org>`_ URL
        - Check in the HTML if the URL is rendered properly
        - URLs containing ``(`` and ``)`` should have these characters escaped as ``%28`` and ``%29`` respectively
        - Check if the URL works when clicking from the generated HTML. If it works the link can be kept, otherwise consider removing the link.
   * - *other*
     - An unforeseen error occured
     - Manually check if the link is still valid; remove the link if necessary.


