import json

from glob import glob
from data import last, match
from file import exists, join, read, split, write


def find(path, query=None, qtype="all"):
  query = query or {}
  return [i for i in load_all(path) if match(i, query, qtype)]


def load(path, key):
  path = join(path, "%s.json" % key)
  return json.loads(read(path)) if exists(path) else None


def load_all(path):
  pattern = join(path, "*.json")
  paths = [p[:-5] for p in glob(pattern)]  # Strip .json
  parts = [split(p) for p in paths]
  ids = [last(p) for p in parts]
  for i in ids:
    yield load(path, i)


def save(path, data, key="id"):
  path = join(path, "%s.json" % data[key])
  write(path, json.dumps(data, indent=2, sort_keys=True))


def save_all(path, data, key="id"):
  for item in data:
    save(path, item, key=key)
