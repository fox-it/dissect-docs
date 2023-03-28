Style guide
===========

This is a basic style guide for the Dissect projects. The goal of this guide is to help improve the quality of the code
by making it more uniform in appearance which should increase the understandability and maintainability. When submitting
code for inclusion in one of the Dissect projects, it helps to follow this guide. This will make the reviewing process
easier and reduces the number of iterations to get it the code in a mergable shape.

Although certain style checks are enforced in the build pipeline, the current code does not always adhere to
all these guidelines. The reason for the latter is that Dissect contains code that was written a long time before this guide
was developed. Changing existing code to match this style guide is a continuous process, but new code should definitely
follow this guide.

A note on refactoring
---------------------

For the parts of these guidelines which are not enforced by our build pipeline we generally deal with them in the
following way. As a rule, new code should always strive to follow these guidelines. For code that gets modified and
is not yet fully following these guidelines, there are the following options:

- If the change is large, it is best to refactor the function, method or class according to these guidelines.
- If the change is minor, or if it wouldn't fit in the context of the rest of the code in the class, file or sub-project, refactoring for things like type hinting
and adding docstrings may be postponed until a larger change or refactor.

Paramount however is that the change you make is understandable and clear in its functioning.

PEP 8 and Black
---------------

The code should adhere to the `PEP 8 <https://peps.python.org/pep-0008/>`_ Python code style. The adherence to PEP 8
is checked using `Flake8 <https://flake8.pycqa.org/>`_. As PEP 8 is not completely unambiguous and Flake8 also makes
certain choices as to how to interpret it, we decided to ignore all flake ``E203`` errors
(see `<https://github.com/PyCQA/pycodestyle/issues/373>`_).

We also set the line limit at 120 characters. For modern console sizes this gives a bit more room compared to the
standard 80 character limit without sacrificing readability, probably even increasing it.

The formatting of the code layout is further refined by using `Black <https://black.readthedocs.io/en/stable/>`_. This is
done for a number of reasons: to have a way to automatically format the code, to have it be consistent between files and
projects regardless of the author and, most importantly, to not have to spend energy on thinking what the exact formatting
should be.

PEP 8 and Black styles are mandatory. This is configured in the project's ``tox.ini`` files and tested for by our build pipeline.

Import order
------------

When importing other modules or files we group the imports into 3 groups. First are the builtin modules, next the modules
from external projects *including* other Dissect projects, e.g. PyYAML, and finally the modules from the project itself.
The imports within the 3 groups should be in alphabetical order, as in the example below:

.. code-block:: python

    import builtins_a
    from builtins_a import foo
    import builtins_b

    import externals_a
    from externals_a import bar
    import externals_b
    import other_dissect_project

    import this_dissect_project
    from this_dissect_project import bla


Type hinting
------------

New functions and classes should be fully type hinted. The combination of type hinting and docstrings helps in understanding
what the function or class does and how it should be used.

Docstring style
---------------

Functions and classes should have docstrings detailing what that function or class does and/or how it should be used. We
follow the `Google docstring format <https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings>`_ and
use the ``sphinx-apidoc`` tool to automatically generate the API documentation.

The first line of a docstring should contain a short sentence describing the nature of the function/class, followed by an
empty line and optionally a more verbose explanation detailing how the function/class goes about doing its thing and/or how
it should be used. Finally, add an indented list of arguments, return value(s) and exceptions which can be raised according
to the Google docstring format. Typing of these parameters should be done through type hinting.

An example of how to use the docstring to comment a function/method.

.. literalinclude:: codestyle.py

The examples above look like this:

.. automodule:: codestyle
    :members:

The most important takeaways are:

* Use ``typehints`` so type information gets automatically added to the documentation
* ``Args:`` To document parameters
* ``Returns:`` To document what it specifically returns
* ``Raises:`` To document if it raises a specific exception and why

Misc styling recommendations
----------------------------

Tuples and Black
~~~~~~~~~~~~~~~~

As Black tries to cram as much content on a single line as possible, it may sometimes interfere with aesthetics. One instance
is when you want a tuple of items formatted over multiple lines. To prevent them from being put on a single line by Black is
to add a comma (``,``) after the last item of the tuple, like this:

.. code-block:: python

    function(
        param1,
        param2,
    )

Coincidentally, this also gives cleaner code diffs when adding or removing items from the tuple later on.

Naming variables
~~~~~~~~~~~~~~~~

Naming variables is always a hard problem. A short list to think of when naming variables:

* Single-character variable names are frowned upon.
* Variables which are named after their type (list, dict etc.) are generally not a good choice.

dissect.cstruct definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using ``dissect.cstruct`` to define and load C structures, split the definition of the structure and the loading of the
structure:

.. code-block:: python

    c_def = """
    #define   SOME_C_DEF = 1
    """

    c_obj = cstruct.load(c_def)

This increases readability and allows you to add a ``# noqa: E501`` after the string defining the C structure. This is useful
if the definition comes from an external source which has lines that are too long, but you want to keep the original layout.

When writing structure definitions for a new parser, try to keep the structure style similar to the original structures, if
possible.

If open-source or openly documented structures are available, use them as much as possible. Changing field types or slightly
altering structures for performance or compatibility reasons is encouraged. For example, ``char[n]`` is faster than ``int8[n]``,
or changing a ``GUID field_name`` to ``char field_name[16]``.

If no original structures are available, make an educated guess on what they could look like in the original source.
For example, during reverse engineering you see a debug log message that uses ``lowerCamelCase`` field names, use that
style for your field names.

If no discernible style is visible, you can use the following general rules:

* For a Microsoft file format, use ``UPPERCASE_NAME`` structure names and ``CamelCase`` field names.

  * One exception is that we generally remove field prefixes like ``dw`` and ``cb``, even when copy-pasting structures.

* For other file formats, use ``lowercase_name`` structure and field names.

Not every parser in ``dissect`` currently adheres to this style, but we try to adhere to these rules for future parsers.

Test cases
----------

We try to unit test as much of the code as possible. As this project originally evolved without a lot of test cases, it is
a sort of catch-up game. New code and large refactors should have unit tests accompanying the changes.

Commit style, tags and branches
-------------------------------

All development should be done on so-called feature branches. Each branch must contain only a single feature or change.
These branches are rebased and squashed on top of the ``main`` branch. The idea is to have the ``main`` branch always in
a (more or less) releasable state.

Commit messages should adhere to the following points:

* Separate subject from body with a blank line
* Limit the subject line to 50 characters as much as possible
* Capitalize the subject line
* Do not end the subject line with a period
* Use the imperative mood in the subject line
* The verb should represent what was accomplished (Create, Add, Fix etc)
* Wrap the body at 72 characters
* Use the body to explain the what and why vs. the how

An example of a commit message:

.. code-block:: text

    Fix parsing extra NULL bytes in the NTFS header

    Sometimes extra null bytes can be present at the end of the NTFS allocator
    table, this patch makes sure they are not included in the next header
    structure.

When the ``main`` branch gets released, it is tagged with a version in the form of ``x.y``. This version is not strictly
a semantic version number. The ``x`` is more like an epoch and the ``y`` an iteration number. There are no compatibility
guarantees between the different Python packages with the same ``x`` version. Only the set of packages at the time of
release should be expected to work well together. This set of packages is codified in a release of the ``dissect`` Python
package through the requirements in its ``setup.py``.
