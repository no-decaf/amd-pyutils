"""Functions for working with errors and exceptions."""

import sys
import traceback


def info():
  """Get a dict containing information about the last exception.

  @return: A dict containing the error traceback, type, and value.
  @rtype: dict
  """

  exc_type, value, tb = sys.exc_info()
  return {
    "traceback": traceback.format_tb(tb),
    "type": str(exc_type),
    "value": str(value)
  }
