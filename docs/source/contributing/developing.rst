Developing for Dissect
======================

.. tip::

    Thinking about writing your own Dissect module? Awesome! We kindly ask that you use the ``dissect.contrib.*`` namespace!



We very much welcome contributions from the community that improve Dissect. Before making your first contribution, we
ask you to read our documentation on the development process, style guide and tooling carefully as they will help you make the contributing process as easy as possible.

These pages are organized as follows:

- `Development process`_: information regarding the development process, including branching, review process and expectations on testing.

- :doc:`Style guide </contributing/style-guide>`: information on how to style code and documentation for a uniform style across all Dissect projects.

- :doc:`Tooling </contributing/tooling>`: information regarding the available tooling for building and testing code and documentation.


Path resolution policy
----------------------

Starting from Dissect version 3.11, we decided that new plugins will only provide the original parsed ``path`` value in its records.
We recommend external contributors to follow the same policy.
This keeps the information inside the records as close to the truth as possible.

A resolved path can still be accessed by using the ``--resolve`` or ``--hash`` flags in :doc:`target-query </tools/target-query>`.
ese flags add additional fields to the record using the identifier/name of the field as a prefix making it easier to identify its origin.
For example, lets say we have a record with the following field:

.. code-block::

    some_name=%SystemRoot%\Temp\file


When using ``--resolve``, the resolved path will be added to the record in a new field with the suffix ``_resolved``:

.. code-block::

    some_name=%SystemRoot%\Temp\file
    some_name_resolved=C:\Windows\Temp\file


While the ``--hash`` flag adds extends the ``--resolve`` information and includes the ``digest`` to it.

.. code-block::

    some_name=%SystemRoot%\Temp\file
    some_name_resolved=C:\Windows\Temp\file
    some_name_digest=(...,...,...)


Development process
-------------------


Python and tox versions
~~~~~~~~~~~~~~~~~~~~~~~

.. include:: /versions.rst


To build and test Dissect projects, `tox <https://tox.wiki/en/latest/>`_ is used.
A minimum version of 4.2.4 is required (when using ``tox`` version 3.3.0 or higher,
it will automatically bootstrap to this minimum version).

More information on available tooling can be found on the :doc:`tooling </contributing/tooling>` page.


Style guide
~~~~~~~~~~~

Dissect has a :doc:`style guide </contributing/style-guide>` for code, documentation and commit messages.
It helps to improve the quality of the code by making it more uniform in appearance which should increase the understandability and
maintainability. It will also make the reviewing process easier and reduces the number of iterations to get the code in
a mergeable shape.

Branching
~~~~~~~~~

Each project has a ``main`` branch. The ``HEAD`` of this ``main`` branch is the potential release candidate for the project.

Development is done on feature branches. When making changes, create a feature branch with a useful and short
name like ``feature/some_new_awesome_feature`` or ``fix/some_bug_fix``. Using a namespace prefix like ``feature/`` or
``fix/`` keeps different types of changes clear.

Feature branches should contain only a single, self-contained, feature or fix. On acceptance, the commits
in the feature branch will be squashed into a single commit. If there are reasons to deviate from this, each *commit* on
the feature branch should contain a single, self-contained, feature or fix. Also make sure to discuss up front if you
think there is reason to deviate from the single feature/fix per feature branch.

Submission and review process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you have finished work in your feature branch and the unit tests and linting tests pass, you can submit
a pull request.

Each pull request will be reviewed before including it in the official code base. Before manual review takes place,
we will run our CI pipeline which executes unit tests and formatting checks. If your pull request does not pass these tests, manual
review will not commence.

If the pull request is accepted, the commit will be merged into the ``main`` branch.
Your contribution will then be incorporated in the next release.

Contributor License Agreement
"""""""""""""""""""""""""""""

We require all contributors to accept our Contributor License Ageement (CLA) before including contributions into our code base.
The process of accepting the agreement is very simple and is only required once:

1. Submit your pull request
2. If this is your first submission, a comment on your pull request will be posted by our DissectBot with the CLA text
3. When you agree with the terms and conditions you reply with a GitHub comment as shown in the CLA text.

Once you have accepted the CLA, the pull request will be processed.

Any future pull requests from the same account will be processed immediately.

Dependencies
~~~~~~~~~~~~

Dissect has a policy of 'least dependencies', meaning that the number of dependencies on other Python packages should be as small
as possible. This limits licensing issues and keeps the software supply chain manageable.

Dissect already has a curated set of dependencies covering a lot of functionality. When adding new dependencies to Dissect, please
add the reason for doing so in a commit message.

Dependencies should be added to ``pyproject.toml``.

Test cases
~~~~~~~~~~

New code and large refactors should have unit tests accompanying the changes even though not all existing code currently has unit tests.
See :doc:`tooling </contributing/tooling>` for information on how to execute test cases.


Documentation
~~~~~~~~~~~~~

Each project generates its own API reference documentation from the docstrings in the code using ``sphinx-autoapi``.
All this documentation will be included under the 'API Reference' header on https://docs.dissect.tools.

The :doc:`style guide </contributing/style-guide>` explains how to format the docstrings for a uniform styling across
all the different projects.

There is also tooling to preview and check the auto-generated API documentation before submitting your code which
is described in :doc:`tooling </contributing/tooling>`.

Releases and versioning
~~~~~~~~~~~~~~~~~~~~~~~

Releases are done by the Dissect core team. Each release has a unique version number.

New releases are made from the ``main`` branch. Once a release is done, that version of the code is tagged with a version number.
Version numbers are of the form ``x.y``, where

- ``x`` is an epoch number
- ``y`` is an iteration number.

There are no compatibility
guarantees between the different Python packages with the same ``x`` version. Only a fixed set of packages at the time of
release should be expected to work well together. This set of packages is published in a release of the ``dissect`` Python
package through the requirements in its ``pyproject.toml`` file.