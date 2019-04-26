"""Functions for working with dicts."""

import flatten_json
import fnmatch

from flatten_json import flatten as _flatten, unflatten_list
from itertools import chain
from amd_pyutils.str import camel_to_snake, snake_to_camel

try:
  from collections.abc import Iterable
except ImportError:
  from collections import Iterable

# Monkeypatch flatten_json because it fails on unicode.
flatten_json._unflatten_asserts = lambda _, __: None


def diff(dct1, dct2):
  """Get the difference between 2 dicts.

  @param dct1: The first dict to compare.
  @type dct1: dict
  @param dct2: The second dict to compare.
  @type dct2: dict

  @return: A tuple with the items unique to dict 1, the items unique to dict 2, and the items common
           to both.
  @rtype: tuple[dict, dict, dict]
  """

  dct1_set = set(flatten(dct1).items())
  dct2_set = set(flatten(dct2).items())
  dct1_unique = dct1_set - dct2_set
  dct2_unique = dct2_set - dct1_set
  common = dct1_set.intersection(dct2_set)

  return unflatten(dict(dct1_unique)), unflatten(dict(dct2_unique)), unflatten(dict(common))


def find(itr, qry, qtype="all"):
  """Find dicts which match the query object.

  @param itr: An iterable containing dicts.
  @type itr: collections.abc.Iterable
  @param qry: A query dict containing key-value pairs to match against.
  @type qry: dict
  @param qtype: The type of query: [all, any, none]
  @type qtype: str

  @return: A list of the dicts that match the query.
  @rtype: list[dict]
  """

  return [i for i in itr if match(i, qry, qtype=qtype)]


def flatten(dct, sep="."):
  """Recursively flatten a dict.

  @param dct: The dict to flatten.
  @type dct: dict
  @param sep: The separator.
  @type sep: str

  @return: A flattened dict.
  @rtype: dict
  """

  return _flatten(dct, sep)


def keys_to_camel(obj):
  """Recursively convert dict keys in an object to camel case.

  @param obj: An object containing dictionaries to convert.
  @type obj: object

  @return: The object, with dict keys converted to camel case.
  @rtype: object
  """

  if isinstance(obj, dict):
    return {snake_to_camel(k): keys_to_camel(v) for k, v in obj.items()}

  if isinstance(obj, Iterable) and not isinstance(obj, str):
    return [keys_to_camel(v) for v in obj]

  return obj


def keys_to_snake(obj):
  """Recursively convert dict keys in an object to snake case.

  @param obj: An object containing dictionaries to convert.
  @type obj: object

  @return: The object, with dict keys converted to snake case.
  @rtype: object
  """

  if isinstance(obj, dict):
    return {camel_to_snake(k): keys_to_snake(v) for k, v in obj.items()}

  if isinstance(obj, Iterable) and not isinstance(obj, str):
    return [keys_to_snake(v) for v in obj]

  return obj


def match(dct, qry, qtype="all"):
  """Determine whether a dict matches a query object.

  @param dct: The dict to match.
  @type dct: dict
  @param qry: A query dict containing key-value pairs to match against.
  @type qry: dict
  @param qtype: The type of query: [all, any, none]
  @type qtype: str

  @return: True if the dict matches the query, otherwise false.
  @rtype: bool
  """

  if qtype not in ("all", "any", "none"):
    raise ValueError("Invalid query type")

  query_set = set(flatten(qry).items())
  dct_set = set(flatten(dct).items())
  if qtype == "all":
    return query_set.issubset(dct_set)
  elif qtype == "any":
    return len(query_set.intersection(dct_set)) > 0
  elif qtype == "none":
    return not query_set.intersection(dct_set)

  raise ValueError("Could not evaluate query type")


def project(dct, key_patterns):
  """Project a dict to a set of key patterns. Supports Unix shell wildcards and dot notation.

  @param dct: The dict to project.
  @type dct: dict
  @param key_patterns: An iterable of key patterns to match.
                       Unix shell-style wildcards and dot notation are allowed.
  @type key_patterns: collections.abc.Iterable[str]

  @return: The projection of the dict.
  @rtype: dict
  """

  flat_dct = flatten(dct)
  matching_keys = chain.from_iterable([fnmatch.filter(flat_dct.keys(), i) for i in key_patterns])
  unique_matching_keys = set(matching_keys)
  projection = {k: v for k, v in flat_dct.items() if k in unique_matching_keys}

  return unflatten(projection)


def unflatten(dct, sep="."):
  """Recursively unflatten a dict.

  @param dct: The dict to flatten.
  @type dct: dict
  @param sep: The separator.
  @type sep: str

  @return: An unflattened dict.
  @rtype: dict
  """

  return unflatten_list(dct, sep)


def unique(itr):
  """Get unique dicts from an iterable.

  @param itr: An iterable containing dicts.
  @type itr: collections.abc.Iterable

  @return: A list of unique dicts from the iterable.
  @rtype: list[dict]
  """

  unique_tuples = set([tuple(flatten(i).items()) for i in itr])

  return [unflatten(dict(i)) for i in unique_tuples]
