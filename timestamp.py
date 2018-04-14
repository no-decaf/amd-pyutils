import calendar
import pytz
import time

from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta


def fromdt(dt):
  """Convert a datetime to a Unix timestamp"""

  # If the datetime is not naive and not UTC
  if dt.tzinfo and dt.tzinfo != pytz.UTC:
    dt = dt.astimezone(pytz.UTC)

  return calendar.timegm(dt.timetuple())


def future(start=None, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
  """Get a future timestamp from a starting timestamp or the current timestamp"""

  start = datetime.utcfromtimestamp(start) if start else datetime.utcnow()
  end = start + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes,
                              seconds=seconds)

  return fromdt(end)


def now():
  """Get the current Unix timestamp"""

  return int(time.time())


def parsedt(dt_str):
  """Parse a datetime string to a Unix timestamp"""

  dt = parser.parse(dt_str)

  return fromdt(dt)


def past(start=None, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
  """Get a past timestamp from a starting timestamp or the current timestamp"""

  start = datetime.utcfromtimestamp(start) if start else datetime.utcnow()
  end = start - relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes,
                              seconds=seconds)

  return fromdt(end)
