"""Functions for working with objects."""

from collections.abc import Iterable
from datetime import date, datetime, time, timedelta, tzinfo
from typing import Any

from amd.util import json

BASE_TYPES = (
    bytes,
    bytearray,
    complex,
    dict,
    float,
    frozenset,
    int,
    list,
    memoryview,
    range,
    set,
    tuple,
)
"""The base types used for converting object values to a dict."""

TIME_TYPES = (date, datetime, time, timedelta, tzinfo)
"""The date/time types used for converting object values to a dict."""


def to_dict(obj: Any) -> Any:  # pylint: disable=R0911
    """Recursively convert an object to a dict.

    NOT FOR PRODUCTION. This is meant for easily serializing objects during
    debugging.

    :param obj: The object to convert.

    :return: The dict equivalent of the object.
    """
    # Try the brute force method.
    try:
        return json.loads(json.dumps(obj))
    except (TypeError, ValueError):
        pass

    if any(isinstance(obj, i) for i in TIME_TYPES) or isinstance(obj, str):
        return obj

    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}

    if hasattr(obj, "__dict__") and vars(obj):
        return {
            k: to_dict(v)
            for k, v in vars(obj).items()
            if not callable(v) and not k.startswith("__")
        }

    if isinstance(obj, Iterable):
        return [to_dict(i) for i in obj]

    if not any(isinstance(obj, i) for i in BASE_TYPES):
        attrs = [
            i
            for i in dir(obj)
            if not i.startswith("__") and not callable(getattr(obj, i))
        ]
        if attrs:
            return {i: getattr(obj, i) for i in attrs}

    return obj
