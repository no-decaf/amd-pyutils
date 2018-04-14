import json
import sys


def pflush(output):
  sys.stdout.write(output)
  sys.stdout.flush()


def pjson(data):
  print json.dumps(data, indent=2, sort_keys=True)
