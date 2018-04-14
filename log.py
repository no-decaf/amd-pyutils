import logging
import json
import sys
import traceback

from file import ensure, filename
from functools import wraps
from logging import FileHandler, Formatter, StreamHandler
from timestamp import now


def configure(file_level=None, file_path=None, stream_level=None):
  """Configure JSON logging to handlers for a file or stream"""

  root_logger = logging.getLogger()
  for handler in root_logger.handlers:
    root_logger.removeHandler(handler)  # Remove any default handlers to avoid duplicate stdout logs
  root_logger.setLevel(logging.DEBUG)

  if file_level:
    if file_path:
      ensure(file_path.replace(filename(file_path), ""))
    else:
      file_path = "%s.log" % now()
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
  def __init__(self, *args, **kwargs):
    logging.Formatter.__init__(self, *args, **kwargs)

  def format(self, record):
    dic = {
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
      dic["exc_info"]["traceback"] = traceback.format_tb(record.exc_info[2])
      dic["exc_info"]["type"] = str(record.exc_info[0])
      dic["exc_info"]["value"] = str(record.exc_info[1])

    return json.dumps(dic, sort_keys=True)
