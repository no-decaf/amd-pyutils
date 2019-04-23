"""Functions for working with strings."""

import re

ALL_CAPS_REGEX = re.compile("([a-z0-9])([A-Z])")
FIRST_CAP_REGEX = re.compile("(.)([A-Z][a-z]+)")


def snake_to_camel(string):
  """Convert a snake case string to camel case.

  @param string: A snake case string to convert to camel case.
  @type string: str

  @return: A camel case string.
  @rtype: str
  """

  parts = string.split("_")
  if len(parts) == 1:
    return parts[0]

  return parts[0] + "".join(i.title() for i in parts[1:])


def camel_to_snake(string):
  """Convert a camel case string to snake case.

  @param string: A snake case string to convert to camel case.
  @type string: str

  @return: A camel case string.
  @rtype: str
  """

  partial_snake_case = FIRST_CAP_REGEX.sub(r"\1_\2", string)

  return ALL_CAPS_REGEX.sub(r"\1_\2", partial_snake_case).lower()
