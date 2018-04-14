import re

from copy import deepcopy

ALL_CAPS_REGEX = re.compile("([a-z0-9])([A-Z])")
FIRST_CAP_REGEX = re.compile("(.)([A-Z][a-z]+)")


def camel(source):
  """Recursively convert dictionary keys in the source to camel case"""

  res = deepcopy(source)  # Default return value

  if isinstance(source, list) or isinstance(source, set):
    res = [camel(v) for v in source]

  elif isinstance(source, dict):
    res = {}
    for k, v in source.items():
      parts = k.split("_")
      k = parts[0] + "".join(x.title() for x in parts[1:])
      res[k] = camel(v)

  return res


def snake(source):
  """Recursively convert dictionary keys in the source to snake case"""

  res = deepcopy(source)  # Default return value

  if isinstance(source, list) or isinstance(source, set):
    res = [snake(v) for v in source]

  elif isinstance(source, dict):
    res = {}
    for k, v in source.items():
      k = FIRST_CAP_REGEX.sub(r"\1_\2", k)
      k = ALL_CAPS_REGEX.sub(r"\1_\2", k).lower()
      res[k] = snake(v)

  return res
