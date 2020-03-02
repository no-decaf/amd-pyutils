"""Functions for working with strings."""

import re

ALL_CAPS_REGEX = re.compile(r"([a-z0-9])([A-Z])")
"""A regular expression to find all of the capital letters in a string."""

FIRST_CAP_REGEX = re.compile(r"(.)([A-Z][a-z]+)")
"""A regular expression to find the first capital letter in a string."""


def camel_to_snake(string: str) -> str:
    """Convert a camel case string to snake case.

    :param string: A snake case string to convert to camel case.

    :return: A snake case string.
    """
    partial_snake_case = FIRST_CAP_REGEX.sub(r"\1_\2", string)

    return ALL_CAPS_REGEX.sub(r"\1_\2", partial_snake_case).lower()


def snake_to_camel(string: str) -> str:
    """Convert a snake case string to camel case.

    :param string: A snake case string to convert to camel case.

    :return: A camel case string.
    """
    parts = string.split("_")
    if len(parts) == 1:
        return parts[0]

    return parts[0] + "".join(i.title() for i in parts[1:])
