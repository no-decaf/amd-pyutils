"""Functions for JSON serialization that support dates and datetimes.

Serialization provides ISO-8601 formatted datetime values.
Deserialization provides date and datetime objects.
"""

import json

from datetime import date, datetime


def dumps(obj):
  """Serialize an object to a JSON-formatted string.

  @param obj: An object that can be serialized to JSON.
  @type obj: object

  @return: A JSON-formatted string.
  @rtype: str
  """

  return json.dumps(obj, default=_default)


def loads(json_str):
  """Deserialize an object from a JSON-formatted string.

  @param json_str: A JSON-formatted string.
  @type json_str: str

  @return: An object that can be serialized to JSON.
  @rtype: object
  """

  return json.loads(json_str, object_hook=_object_hook)


def readable(obj):
  """Serialize an object to a readable JSON-formatted string.

  @param obj: An object that can be serialized to JSON.
  @type obj: object

  @return: A readable JSON-formatted string.
  @rtype: str
  """

  return json.dumps(obj, default=_default, indent=2, sort_keys=True)


def _default(obj):
  """A default implementation for json.dumps that handles date and datetime values.

  @param obj: An object that can be serialized to JSON.
  @type obj: object

  @return: An ISO-8601 formatted value if the object is a date or datetime.
  @rtype: str | None
  """

  if isinstance(obj, (date, datetime)):
    return obj.isoformat()


def _object_hook(dct):
  """An object hook for json.loads that handles date and datetime values.

  @param dct: An dict that has been deserialized from JSON.
  @type dct: dict

  @return: The modified dict with date and datetime values deserialized.
  @rtype: dict
  """

  for k, v in dct.items():
    if isinstance(v, str):
      parsed = False

      # datetime will parse date values, but date will not parse datetime values.
      # So try to parse date first.
      try:
        dct[k] = date.fromisoformat(v)
        parsed = True
      except (TypeError, ValueError):
        pass

      if not parsed:
        try:
          dct[k] = datetime.fromisoformat(v)
        except (TypeError, ValueError):
          pass

  return dct
