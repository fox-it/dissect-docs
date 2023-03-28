Developing for Dissect
======================

.. tip::

    Thinking about writing your own Dissect module? Awesome! We kindly ask that you use the ``dissect.contrib.*`` namespace!

Development
-----------

Dissect is built and tested against Python 3.9 (CPython and PyPy). Older versions may not work, as features are used which
may not yet be supported by these versions (for example ``@cached_property`` is only supported since Python 3.9).
Newer versions will probably work, but are not guaranteed to.

To build and test Dissect projects, `tox <https://tox.wiki/en/latest/>`_ is used. A minimum version of 3.8 is required.

When developing for Dissect, please make sure you follow :doc:`the style guide </contributing/style-guide>`. It helps to
improve the quality of the code by making it more uniform in appearance which should increase the understandability and
maintainability. It will also make the reviewing process easier and reduces the number of iterations to get the code in
a mergable shape.

Branches & Tags
~~~~~~~~~~~~~~~

Development is done on so-called feature branches. When making changes, create a feature branch with a useful and short
name like ``feature/some_new_awsome_feature`` or ``fix/some_bug_fix``. Using a namespace prefix like ``feature/`` or
``fix/`` keeps different types of changes clear.

When you are done with building the feature or creating the fix, do a final run of the unit tests and linting and make a
pull request. The code will be reviewed and tested again in our CI pipeline.

Be aware that a feature branch should contain only a single, self-contained, feature or fix. On acceptance, the commits
in the feature branch will be squashed into a single commit. If there are reasons to deviate from this, each *commit* on
the feature branch should contain a single, self-contained, feature or fix. Also make sure to discuss up front if you
think there is reason to deviate from the single feature/fix per feature branch.

If the pull request is accepted, the commit will be merged into the ``main`` branch. The ``HEAD`` of this branch is the potential
release candidate for the project. Once a release is done, it will be tagged with a version number.

Building & testing
------------------

The build uses PEP 517 and PEP 518. Together with ``tox``'s ``isolated_build`` feature this ensures there are no hidden
dependencies on locally installed packages.

The ``tox.ini`` configuration file together with the ``pyproject.toml`` and ``setup.py`` files will make sure the correct
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
