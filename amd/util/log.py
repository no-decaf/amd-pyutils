"""Functions for working with logging."""

import logging
import os
import sys
import traceback
from datetime import datetime
from functools import wraps
from logging import FileHandler, Formatter, Logger, StreamHandler
from typing import Any, Callable

from amd.util import json


def configure(
    file_level: int = None, file_path: str = None, stream_level: int = None
) -> None:
    """Configure logging to send JSON to a file or formatted output to a stream.

    NOT FOR PRODUCTION.

    This is meant for generating useful logs when debugging. It is not meant for
    production use. It will remove default logging handlers from the root logger to
    avoid duplicate STDOUT logs.

    :param file_level: If specified, will log this level of output to a file.
    :param file_path: The path of the log file. Default to the current POSIX timestamp
                      if unspecified.
    :param stream_level: If specified, will log this level of output to STDOUT.
    """
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(
            handler
        )  # Remove default handlers to avoid duplicate stdout logs.
    root_logger.setLevel(logging.DEBUG)

    if file_level:
        if file_path:
            log_file = file_path.replace(os.path.basename(file_path), "")
            if not os.path.exists(log_file):
                os.makedirs(log_file)
        else:
            file_path = "%s.log" % datetime.utcnow().timestamp
        file_handler = FileHandler(file_path, mode="a+")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(JsonFormatter())
        root_logger.addHandler(file_handler)

    if stream_level:
        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(stream_level)
        stream_handler.setFormatter(Formatter("%(levelname)s:%(name)s: %(message)s"))
        root_logger.addHandler(stream_handler)


def log_io(logger: Logger) -> Callable[[Any], Any]:
    """Wrap a function and log input/output at the DEBUG level.

    Input/output must be JSON-serializable.

    :param logger: The logger object to use for writing all input and output.

    :return: A function wrapper.
    """
    # noqa: D202
    def inner_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(
                    {
                        "logger": logger.name,
                        "method": func.__name__,
                        "type": "input",
                        "value": {"args": args, "kwargs": kwargs},
                    }
                )
                res = func(*args, **kwargs)
                logger.debug(
                    {
                        "logger": logger.name,
                        "method": func.__name__,
                        "type": "output",
                        "value": res,
                    }
                )
                return res
            except:  # noqa
                logger.exception({"method": func.__name__})
                raise

        return wrapper

    return inner_wrapper


class JsonFormatter(Formatter):
    """A log formatter to write logs as JSON."""

    def __init__(self, *args, **kwargs):
        """See base class."""
        Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        """See base class."""
        dct = {
            "args": (),
            "created": int(record.created),
            "exc_info": {"traceback": None, "type": None, "value": None},
            "exc_text": record.exc_text,
            "file": record.filename,
            "function": record.funcName,
            "level": record.levelname,
            "line": record.lineno,
            "message": record.msg,
            "module": record.module,
            "name": record.name,
            "path": record.pathname,
        }
        if record.exc_info:
            dct["exc_info"] = {
                "traceback": traceback.format_tb(record.exc_info[2]),
                "type": str(record.exc_info[0]),
                "value": str(record.exc_info[1]),
            }

        return json.dumps(dct)
