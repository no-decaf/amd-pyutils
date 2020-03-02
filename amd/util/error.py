"""Functions for working with errors and exceptions."""

import sys
import traceback
from typing import Dict


def info() -> Dict[str, str]:
    """Get a dict containing information about the last exception.

    :return: A dict containing the error traceback, type, and value.
    """
    exc_type, value, trace = sys.exc_info()
    return {
        "traceback": traceback.format_tb(trace),
        "type": str(exc_type),
        "value": str(value),
    }
