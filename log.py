"""Functions for working with logging."""

import json_ as json
import logging
import os
import sys
import traceback

from datetime import datetime
from functools import wraps
from logging import FileHandler, Formatter, StreamHandler


def configure(file_level=None, file_path=None, stream_level=None):
  """Configure logging to send JSON output to a file or formatted output to a stream. NOT FOR PRODUCTION.

  This is meant for generating useful logs when debugging. It is not meant for production use.
  It will remove default logging handlers from the root logger to avoid duplicate STDOUT logs.

  @param file_level: If specified, will log this level of output to a file.
  @type file_level: int
  @param file_path: The path of the log file. Will default to the current POSIX timestamp if unspecified.
  @type file_path: str
  @param stream_level: If specified, will log this level of output to STDOUT.
  @type stream_level: int
  """

  root_logger = logging.getLogger()
  for handler in root_logger.handlers:
    root_logger.removeHandler(handler)  # Remove any default handlers to avoid duplicate stdout logs.
  root_logger.setLevel(logging.DEBUG)

  if file_level:
    if file_path:
      log_file = file_path.replace(os.path.basename(file_path), "")
      if not os.path.exists(log_file):
        os.makedirs(log_file)
    else:
      file_path = "%s.log" % datetime.utcnow().timestamp
    fh = FileHandler(file_path, mode="a+")
    fh.setLevel(file_level)
    fh.setFormatter(JsonFormatter())
    root_logger.addHandler(fh)

  if stream_level:
    sh = StreamHandler(stream=sys.stdout)
    sh.setLevel(stream_level)
    sh.setFormatter(Formatter("%(levelname)s:%(name)s: %(message)s"))
    root_logger.addHandler(sh)


def log_io(logger):
  """A wrapper that will log input/output from a function at the DEBUG level. Input/output must be JSON-serializable.

  @param logger: The logger object to use for writing all input and output.
  @type logger: logging.Logger

  @return: A function wrapper.
  @rtype: function
  """

  def inner_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        logger.debug({
          "logger": logger.name,
          "method": func.__name__,
          "type": "input",
          "value": {"args": args, "kwargs": kwargs}
        })
        res = func(*args, **kwargs)
        logger.debug({
          "logger": logger.name,
          "method": func.__name__,
          "type": "output",
          "value": res
        })
        return res
      except:
        logger.exception({"method": func.__name__})
        raise

    return wrapper

  return inner_wrapper


class JsonFormatter(logging.Formatter):
  """A formatted for writing logs as JSON."""

  def __init__(self, *args, **kwargs):
    logging.Formatter.__init__(self, *args, **kwargs)

  def format(self, record):
    dct = {
      "args": (),
      "created": int(record.created),
      "exc_info": {
        "traceback": None,
        "type": None,
        "value": None
      },
      "exc_text": record.exc_text,
      "file": record.filename,
      "function": record.funcName,
      "level": record.levelname,
      "line": record.lineno,
      "message": record.msg,
      "module": record.module,
      "name": record.name,
      "path": record.pathname
    }
    if record.exc_info:
      dct["exc_info"]["traceback"] = traceback.format_tb(record.exc_info[2])
      dct["exc_info"]["type"] = str(record.exc_info[0])
      dct["exc_info"]["value"] = str(record.exc_info[1])

    return json.dumps(dct)
