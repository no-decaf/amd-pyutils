import json


def todict(obj):
  """Recursively convert an object into a dictionary"""

  try:
    return json.loads(json.dumps(obj))
  except:
    pass

  if isinstance(obj, dict):
    return {k: todict(v) for k, v in obj.items()}

  if hasattr(obj, "_ast"):
    return todict(obj._ast())

  if hasattr(obj, "__iter__"):
    return [todict(v) for v in obj]

  if hasattr(obj, "__dict__") and obj.__dict__:
    return {
      k: todict(v) for k, v in obj.__dict__.items()
      if not callable(v) and not k.startswith("_")
    }

  if type(obj) not in (basestring, dict, float, int, list, long, set, tuple) \
      and hasattr(obj, "__str__"):
    return str(obj)

  return obj
