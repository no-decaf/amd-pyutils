"""Functions for working with dicts."""

import fnmatch
from itertools import chain
from typing import Any, Dict, Iterable, List, Tuple

import flatten_json
from flatten_json import flatten as _flatten
from flatten_json import unflatten as _unflatten

# Monkeypatch flatten_json because it fails on unicode.
flatten_json._unflatten_asserts = lambda _, __: None  # pylint: disable=W0212


def diff(
    dct1: Dict[str, Any], dct2: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Get the difference between 2 dicts.

    :param dct1: The first dict to compare.
    :param dct2: The second dict to compare.

    :return: A tuple with the items unique to dict 1, the items unique to dict
             2, and the items common to both.
    """
    dct1_set = set(flatten(dct1).items())
    dct2_set = set(flatten(dct2).items())
    dct1_unique = dct1_set - dct2_set
    dct2_unique = dct2_set - dct1_set
    common = dct1_set.intersection(dct2_set)

    return (
        unflatten(dict(dct1_unique)),
        unflatten(dict(dct2_unique)),
        unflatten(dict(common)),
    )


def find(
    obj: Any, qry: Dict[str, Any], qtype: str = "all"
) -> List[Dict[str, Any]]:
    """Recursively find dicts which match the query object.

    :param obj: An object containing dictionaries to search.
    :param qry: A query dict containing key-value pairs to match against.
    :param qtype: The type of query: [all, any, none]

    :return: A list of the dicts that match the query.
    """
    matches = []

    if isinstance(obj, dict):
        if match(obj, qry, qtype):
            matches.append(obj)
        matches.extend(
            chain.from_iterable([find(v, qry, qtype) for v in obj.values()])
        )

    if isinstance(obj, Iterable) and not isinstance(obj, str):
        matches.extend(chain.from_iterable([find(i, qry, qtype) for i in obj]))

    return matches


def flatten(dct: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Recursively flatten a dict.

    :param dct: The dict to flatten.
    :param sep: The separator.

    :return: A flattened dict.
    """
    return _flatten(dct, sep)


def match(dct: Dict[str, Any], qry: Dict[str, Any], qtype: str = "all") -> bool:
    """Determine whether a dict matches a query object.

    :param dct: The dict to match.
    :param qry: A query dict containing key-value pairs to match against.
    :param qtype: The type of query: [all, any, none]

    :return: True if the dict matches the query, otherwise false.
    """
    if qtype not in ("all", "any", "none"):
        raise ValueError("Invalid query type")

    query_set = set(flatten(qry).items())
    dct_set = set(flatten(dct).items())
    if qtype == "all":
        return query_set.issubset(dct_set)
    if qtype == "any":
        return bool(query_set.intersection(dct_set))
    if qtype == "none":
        return not bool(query_set.intersection(dct_set))

    raise ValueError("Could not evaluate query type")


def project(dct: Dict[str, Any], key_patterns: Iterable[str]) -> Dict[str, Any]:
    """Project a dict to key patterns.

    Supports Unix shell wildcards and dot notation.

    :param dct: The dict to project.
    :param key_patterns: An iterable of key patterns to match. Unix shell-style
                         wildcards and dot notation are allowed.

    :return: The projection of the dict.
    """
    flat_dct = flatten(dct)
    matching_keys = chain.from_iterable(
        [fnmatch.filter(flat_dct.keys(), i) for i in key_patterns]
    )
    unique_matching_keys = set(matching_keys)
    projection = {
        k: v for k, v in flat_dct.items() if k in unique_matching_keys
    }

    return unflatten(projection)


def unflatten(dct: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Recursively unflatten a dict.

    :param dct: The dict to flatten.
    :param sep: The separator.

    :return: An unflattened dict.
    """
    return _unflatten(dct, sep)


def unique(itr: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get unique dicts from an iterable.

    :param itr: An iterable containing dicts.

    :return: A list of unique dicts from the iterable.
    """
    unique_tuples = {tuple(flatten(i).items()) for i in itr}

    return [unflatten(dict(i)) for i in unique_tuples]
