import sys
import traceback


def err_info():
  exc_type, value, tb = sys.exc_info()
  return {
    "traceback": traceback.format_tb(tb),
    "type": str(exc_type),
    "value": str(value)
  }
