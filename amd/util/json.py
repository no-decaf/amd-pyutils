"""Functions for JSON serialization that support dates, datetimes, and unicode.

Serialization provides ISO 8601 formatted datetime values with time zones.
Naive datetimes will be localized to UTC to be compliant with ISO 8601.
Deserialization provides Python date and datetime objects.
Any deserialized datetimes that are naive will be localized to UTC.

Since this is primarily used for serializing JSON across API boundaries, the
implementation closely follows the _json implementation from itsdangerous which
is used by Flask.
https://github.com/pallets/itsdangerous/blob/master/src/itsdangerous/_json.py
"""

import json
import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from amd.util.datetime import make_aware

DATETIME_REGEX = re.compile(
    r"^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d+)?(\+\d{2}:\d{2})?$"
)
"""A regular expression to find an ISO 8601 datetime."""

DATE_REGEX = re.compile(r"^\d{4}-[01]\d-[0-3]\d$")
"""A regular expression to find an ISO 8601 date."""


def dumps(obj: Any) -> str:
    """Serialize an object to a compact JSON string.

    :param obj: An object that can be serialized to JSON.

    :return: A JSON string.
    """
    obj = make_aware(obj)

    return json.dumps(
        obj, default=_default, ensure_ascii=False, separators=(",", ":")
    )


def loads(json_str: str) -> Union[Dict[str, Any], List[Any]]:
    """Deserialize an object from a JSON string.

    :param json_str: A JSON string.

    :return: A dict or list.
    """
    obj = json.loads(json_str, object_hook=_object_hook)

    return make_aware(obj)


def readable(obj: Any) -> str:
    """Serialize an object to a readable JSON string.

    :param obj: An object that can be serialized to JSON.

    :return: A readable JSON string.
    """
    obj = make_aware(obj)

    return json.dumps(
        obj, default=_default, ensure_ascii=False, indent=2, sort_keys=True
    )


def _default(obj: Any) -> Optional[str]:
    """Handle date and datetime values for json.dumps.

    :param obj: An object that is being serialized to JSON.

    :return: An ISO 8601 formatted value if the object is a date, else None.
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return None


def _object_hook(dct: Dict[str, Any]) -> Dict[str, Any]:
    """Handle date and datetime values for json.loads.

    :param dct: An dict that has been deserialized from JSON.

    :return: The modified dict with date and datetime values deserialized.
    """
    for key, val in dct.items():
        if isinstance(val, str):

            try:
                if re.match(DATETIME_REGEX, val):
                    dct[key] = datetime.fromisoformat(val)
                elif re.match(DATE_REGEX, val):
                    dct[key] = date.fromisoformat(val)
            except (TypeError, ValueError):
                pass

    return dct
