Style guide
===========

This is a basic style guide for the Dissect projects. The goal of this guide is to increase the understandability and maintainability
of both code and documentation.

Applicability
-------------

This guide is applicable to both new and exisiting code and the Dissect build pipeline enforces the most important rules.
Certain exceptions are made for older parts of the code as they were written before the creation of this guide.

New code
^^^^^^^^

When submitting new code for inclusion in one of the Dissect projects, your code should adhere
to this guide unless there is a valid reason not to do so. This motivation should be added to your eventual
Pull Request.

Older code
^^^^^^^^^^

When submitting changes to existing code that does not yet adhere to this style guide, a choice should be made
whether or not to make the change conformant to the guidelines. You can use the rules below to help you decide
what to do in these cases.

If the change in existing code is

- large, it is best to refactor the function, method or class according to these guidelines.
- small and rewriting the code for guideline conformance would not be proportional to the change itself, you may submit the code using the original styling.

.. note::
    Regardless of conformance to this style guide, any change you make should be understandable and clear in its functioning.


Code style and formatting
-------------------------

This section lists how to format code in a readable and consistent manner and which specifications and tools are used to
enforce them.

PEP 8 and Black
^^^^^^^^^^^^^^^

The code should adhere to the `PEP 8 <https://peps.python.org/pep-0008/>`_ Python code style. The adherence to PEP 8
is checked using `Flake8 <https://flake8.pycqa.org/>`_. Flake ``E203`` errors can be ignored due to the ambigious nature
of these errors (see `<https://github.com/PyCQA/pycodestyle/issues/373>`_).

The formatting of the code layout is further refined by using `Black <https://black.readthedocs.io/en/stable/>`_.
Black provides functionality to automatically format code and enforces consistent coding style between files and projects regardless
of the author. It also relieves authors of the burden of having to actively think about the formatting.

PEP 8 and Black styles are mandatory. This is configured in the project's ``tox.ini`` files and tested for by our build pipeline.

Maximum line length
^^^^^^^^^^^^^^^^^^^

Lines should be limited to 120 characters. For modern console sizes this gives a bit more room compared to the
standard 80 character limit without sacrificing readability, probably even increasing it.

Type hinting
^^^^^^^^^^^^

New functions and classes should be fully type hinted. The combination of type hinting and docstrings helps in understanding
what the function or class does and how it should be used.

Import order
^^^^^^^^^^^^

Import statements for files and modules are divided into three groups and should be ordered as indicated below:

1. builtin modules
2. modules from external projects *including* other Dissect projects, e.g. PyYAML
3. modules from the project itself.

The imports within each group should be in alphabetical order, as in the example below:

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

Formatting tuples
^^^^^^^^^^^^^^^^^

Care should be taken when formatting tuples as Black attempts to reformat all elements into a single line.
To prevent this, add a comma (``,``) after the last item of the tuple, like this:

.. code-block:: python

    function(
        param1,
        param2,
    )

Coincidentally, this also gives cleaner code diffs when adding or removing items from the tuple later on.

Naming variables
^^^^^^^^^^^^^^^^

Naming variables can be challenging. When deciding on a variable name, take the following rules into account:

* Avoid single-character variable names.
* Don't name variables after their type (list, dict etc.).


Incorporating dissect.cstruct definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Writing structure definitions is an essential part of writing a new parser. The following rules show how to
format them properly.

Split definition and loading
""""""""""""""""""""""""""""

When using ``dissect.cstruct`` to define and load C structures, split the definition of the structure and the loading of the
structure:

.. code-block:: python

    c_def = """
    #define   SOME_C_DEF = 1
    """

    c_obj = cstruct.load(c_def)

This increases readability and allows you to add a ``# noqa: E501`` after the string defining the C structure. This is useful
if the definition comes from an external source which has lines that are too long, but you want to keep the original layout.

Styling structure definitions
"""""""""""""""""""""""""""""

The main rule for styling structure definitions is to keep the style similar to the original structures when this is possible.

Below follows more specific rules depending on the availability of the structures:

1. If open-source or openly documented structures are available, use them as much as possible. Changing field types or slightly
altering structures for performance or compatibility reasons is encouraged. For example, ``char[n]`` is faster than ``int8[n]``,
or changing a ``GUID field_name`` to ``char field_name[16]``.

2. If no original structures are available, make an educated guess on what they could look like in the original source.
For example, during reverse engineering you see a debug log message that uses ``lowerCamelCase`` field names, use that
style for your field names.

If no discernible style is visible, you can use the following general rules:

* For a Microsoft file format, use ``UPPERCASE_NAME`` structure names and ``CamelCase`` field names.

  * One exception is that field prefixes like ``dw`` and ``cb`` should be removed, even when copy-pasting structures.

* For other file formats, use ``lowercase_name`` structure and field names.

Documentation style and formatting
----------------------------------

New code needs to be documented properly using docstrings. To understand how documentation
is organised and generated, check out the :doc:`developing for Dissect </contributing/developing>` page.

Use of docstrings
^^^^^^^^^^^^^^^^^

Functions and classes should have docstrings detailing what that function or class does and/or how it should be used. They
should be formatted as described in the `Google docstring format <https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings>`_.

The first line of a docstring should contain a short sentence describing the nature of the function/class, followed by an
empty line and optionally a more verbose explanation detailing how the function/class goes about doing its thing and/or how
it should be used. Finally, add an indented list of arguments, return value(s) and exceptions which can be raised according
to the Google docstring format.

Typing of parameters should be done through type hinting.

Use the ``References:`` clause when referencing external resources such as URLs to websites.

Example docstrings
^^^^^^^^^^^^^^^^^^

An example of how to use the docstring to comment a function/method:

.. literalinclude:: codestyle.py

The examples above look like this:

.. automodule:: codestyle
    :members:

The most important takeaways are:

* Use ``typehints`` so type information gets automatically added to the documentation
* ``Args:`` To document parameters
* ``Returns:`` To document what it specifically returns
* ``Raises:`` To document if it raises a specific exception and why


Commit message style and formatting
-----------------------------------

Commit messages should adhere to the following points:

* Separate subject from body with a blank line
* Limit the subject line to 50 characters as much as possible
* Capitalize the subject line
* Do not end the subject line with a period
* Use the imperative mood in the subject line
* The verb should represent what was accomplished (Create, Add, Fix etc)
* Wrap the body at 72 characters
* Use the body to explain the what and why vs. the how

Example commit message
^^^^^^^^^^^^^^^^^^^^^^

An example of a properly formatted commit message:

.. code-block:: text

    Fix parsing extra NULL bytes in the NTFS header

    Sometimes extra null bytes can be present at the end of the NTFS allocator
    table, this patch makes sure they are not included in the next header
    structure.
