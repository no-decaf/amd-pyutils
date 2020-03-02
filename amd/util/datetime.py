"""Functions for working with datetimes."""

from datetime import datetime
from typing import Any, Iterable

import pytz
from pytz import _FixedOffset


def make_aware(obj: Any, tzinfo: _FixedOffset = pytz.UTC) -> Any:
    """Recusrively make all datetime objects timezone-aware.

    :param obj: A datetime or an object that may contain datetimes.
    :param tzinfo: The timezone to use for localization.

    :return: A timezone-aware datetime or an object containing timezone-aware datetimes.
    """
    if isinstance(obj, dict):
        return {k: make_aware(v, tzinfo=tzinfo) for k, v in obj.items()}

    if isinstance(obj, Iterable) and not isinstance(obj, str):
        return [make_aware(i, tzinfo=tzinfo) for i in obj]

    if isinstance(obj, datetime) and is_naive(obj):
        obj = tzinfo.localize(obj)

    return obj


def make_naive(obj: Any) -> Any:
    """Recusrively make all datetime objects naive.

    :param obj: A datetime or an object that may contain datetimes.

    :return: A naive datetime or an object containing naive datetimes.
    """
    if isinstance(obj, dict):
        return {k: make_naive(v) for k, v in obj.items()}

    if isinstance(obj, Iterable) and not isinstance(obj, str):
        return [make_naive(i) for i in obj]

    if isinstance(obj, datetime) and is_aware(obj):
        obj = obj.replace(tzinfo=None)

    return obj


def is_aware(obj: datetime) -> bool:
    """Check whether a datetime is timezone-aware.

    :param obj: A datetime to check.

    :return: True if the datetime is timezone-aware, otherwise false.
    """
    return obj.tzinfo is not None and obj.tzinfo.utcoffset(obj) is not None


def is_naive(obj: datetime) -> bool:
    """Check whether a datetime is naive.

    :param obj: A datetime to check.

    :return: True if the datetime is naive, otherwise false.
    """
    return obj.tzinfo is None or obj.tzinfo.utcoffset(obj) is None


def utcnow() -> datetime:
    """Create a timezone-aware datetime at the current UTC time.

    :return: A timezone-aware UTC datetime.
    """
    return pytz.UTC.localize(datetime.utcnow())  # pylint: disable=E1120
