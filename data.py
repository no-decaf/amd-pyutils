import flatten_json

from copy import deepcopy
from flatten_json import flatten as _flatten, unflatten_list as _unflatten_list
from itertools import groupby

# Monkeypatch because it fails on unicode
flatten_json._unflatten_asserts = lambda _, __: None


def diff(dic1, dic2):
  """Get the differences between 2 dictionaries"""

  dic1_set = set(flatten(dic1).items())
  dic2_set = set(flatten(dic2).items())
  dic1 = dic1_set - dic2_set
  dic2 = dic2_set - dic1_set

  return unflatten(dict(dic1)), unflatten(dict(dic2))


def find(iterable, query, qtype="all"):
  """Find dictionaries which match the query object"""

  return [i for i in iterable if match(i, query, qtype=qtype)]


def first(iterable):
  """Get the first value from an iterable or return None"""

  return index(iterable, 0)


def flatten(dic, sep="."):
  """Recursively flatten a dictionary"""

  return _flatten(dic, sep)


def group(iterable, key):
  """Group an iterable by dictionary key or grouping function, returning lists instead of generators"""

  res = {}

  by_key = (lambda i: i[key]) if not callable(key) else key

  for k, v in groupby(iterable, key=by_key):
    res[k] = list(v)

  return res


def index(iterable, idx):
  """Get the value from the index of an iterable or return None"""

  return iterable[idx] if iterable and len(iterable) > abs(idx) else None


def last(iterable):
  """Get the last value from an iterable or return None"""

  return index(iterable, -1)


def match(dic, query, qtype="all"):
  """Determine whether a dictionary matches a query object"""

  if qtype not in ("all", "any", "none"):
    raise ValueError("Invalid query type")

  query_set = set(flatten(query).items())
  dic_set = set(flatten(dic).items())
  if qtype == "all":
    return query_set.issubset(dic_set)
  elif qtype == "any":
    return len(query_set.intersection(dic_set)) > 0
  elif qtype == "none":
    return not query_set.intersection(dic_set)

  raise ValueError("Could not evaluate query type")


def notempty(iterable, dicts=True, iterables=True, strings=True):
  """Return elements of an iterable that are not empty"""

  res = []

  for item in iterable:

    if item is None:
      continue

    if dicts and isinstance(item, dict) and not item.keys():
      continue

    if iterables and type(item) in (list, tuple, set) and not item:
      continue

    if strings and isinstance(item, basestring) and not item.strip():
      continue

    res.append(item)

  return res


def patch(source, destination, empty=True):
  """Patch one dictionary with the values from another

  NOTE: This only updates the top-level dictionary and nested dictionaries. Iterable properties are copied over.
  """

  source = source or {}

  if not isinstance(source, dict) or not isinstance(destination, dict):
    raise ValueError("source and destination must be dictionaries")

  res = deepcopy(destination)
  for key in source:
    if not empty and not source[key]:
      continue
    if isinstance(source[key], dict):
      res[key] = patch(source[key], res.get(key, {}) or {}, empty=empty)
    else:
      res[key] = source[key]

  return res


def project(source, schema, partial=False):
  """Project source data to a schema

  Partial projection won't add missing keys from the schema to the source
  """

  if schema == object:
    return source  # Accept anything

  if isinstance(schema, dict):
    source = source if source and isinstance(source, dict) else dict()
    output = dict()
    for key in schema:
      if key in source or not partial:
        output[key] = project(source.get(key), schema[key], partial=partial)
    return output

  if isinstance(schema, list):
    source = source if source and isinstance(source, list) else list()
    return [project(i, schema[0], partial=partial) for i in source]

  if isinstance(schema, set):
    source = source if source and isinstance(source, set) else set()
    return set([project(i, list(schema)[0], partial=partial) for i in source])

  if isinstance(schema, tuple):
    source = source if source and isinstance(source, tuple) else tuple()
    return tuple([project(i, list(schema)[0], partial=partial) for i in source])

  # If the schema is of type dict (not an instance), the output is a dict with any structure
  if schema == dict:
    return source if source and isinstance(source, dict) else dict()

  # If the schema is of type list (not an instance), the output is a list with any contents
  if schema == list:
    return source if source and isinstance(source, list) else list()

  # If the schema is of type set (not an instance), the output is a set with any contents
  if schema == set:
    return source if source and isinstance(source, set) else set()

  # If the schema is of type tuple (not an instance), the output is a tuple with any contents
  if schema == tuple:
    return source if source and isinstance(source, tuple) else tuple()

  return source


def single(iterable):
  """Get a single value from an iterable or return None, erroring if there are multiple values"""

  if iterable and len(iterable):
    if len(iterable) > 1:
      raise ValueError("More than one value in iterable")
    return iterable[0]

  return None


def take(iterable, limit):
  """Take values from an iterable up to a limit"""

  if iterable and len(iterable):
    return [iterable[i] for i in range(limit) if i < len(iterable)]

  return []


def unflatten(dic, sep="."):
  """Recursively unflatten a dictionary"""

  return _unflatten_list(dic, sep)


def unique(iterable):
  """Get unique dictionaries from a list"""

  unique_tuples = set([tuple(flatten(i).items()) for i in iterable])
  return [unflatten(dict(i)) for i in unique_tuples]
