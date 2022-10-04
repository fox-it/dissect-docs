def comment_example(raw_comment: str) -> str:
    """This is an example comment.

    Args:
        raw_comment: A string containing the raw comment

    Returns:
        Data with a ``Comment: `` prefix
    """
    return f"Comment: {raw_comment}"


class CodestyleException(Exception):
    """An exception that gets raised to illustrate this example."""


def function_with_an_exception() -> None:
    """This function raises an exception.

    This function is only for illustratory purposes.

    Raises:
        CodestyleException: Gets raised as an example
    """
    if True:
        raise CodestyleException("Hello")


#: This is a magic random string comment
some_random_variable: str = "hello world"

some_other_way_of_using_a_variable_comment: str = "Hello world 2"
"""Sphinx also recognizes this as a type of comment"""

private_member: str = "Private Member"
"""Using the ``meta private`` directive, you can tell sphinx not to include the variable

:meta private:"""

_public_member: str = "Public Member"
"""Using the ``meta public`` directive, you can tell sphinx to include the variable in the documentation.
When the variable name is prefixed with ``_``, it makes the variable private by default.

:meta public:"""
