"""Functions for working with objects."""

import json_ as json

from collections import Iterable
from datetime import date, datetime, time, timedelta, tzinfo

base_types = (
  basestring, bytes, bytearray, complex, dict, float, frozenset, int, list, long, memoryview, range, set, tuple
)
time_types = (date, datetime, time, timedelta, tzinfo)


def to_dict(obj):
  """Recursively convert an object into a dict. NOT FOR PRODUCTION.

  This is meant for easily serializing objects so they can be inspected. It is not meant for production use.

  @param obj: The object to convert.
  @type obj: object

  @return: The dict equivalent of the object.
  @rtype: dict
  """

  # Try the brute force method.
  try:
    return json.loads(json.dumps(obj))
  except (TypeError, ValueError):
    pass

  if type(obj) in time_types or isinstance(obj, str):
    return obj

  if isinstance(obj, dict):
    return {k: to_dict(v) for k, v in obj.items()}

  if hasattr(obj, "__dict__") and vars(obj):
    return {
      k: to_dict(v) for k, v in vars(obj).items()
      if not callable(v) and not k.startswith("__")
    }

  if hasattr(obj, "_ast"):
    return to_dict(obj._ast())

  if isinstance(obj, Iterable):
    return [to_dict(i) for i in obj]

  if type(obj) not in base_types:
    attrs = [i for i in dir(obj) if not i.startswith("__") and not callable(getattr(obj, i))]
    if attrs:
      return {i: getattr(obj, i) for i in attrs}

  return obj
