import os

from data import notempty


def ensure(path):
  if not os.path.exists(path):
    os.makedirs(path)


def exists(path):
  return os.path.exists(path)


def filename(path):
  return os.path.basename(path)


def folder_path(file_magic_method):
  return os.path.sep.join(file_magic_method.split(os.path.sep)[:-1])


def join(*paths):
  paths = notempty(paths)
  return os.path.sep.join(paths)


def read(path):
  return open(path, "r").read()


def split(path):
  return path.split(os.path.sep)


def write(path, content):
  with open(path, "w+") as out_f:
    out_f.write(content)
