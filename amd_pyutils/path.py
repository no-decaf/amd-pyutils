"""Functions for working with os.path."""

import os


def ensure(path):
  """Ensure the path exists.

  @param path: The path to ensure.
  @type path: str
  """

  if not os.path.exists(path):
    os.makedirs(path)


def exists(path):
  """Determine whether the path exists.

  @param path: The path to check.
  @type path: str

  @return: True if the path exists, otherwise False.
  @rtype: bool
  """

  return os.path.exists(path)


def get_filename(path):
  """Get the filename from the path.

  @param path: The path to check.
  @type path: str

  @return: True if the path exists, otherwise False.
  @rtype: bool
  """

  return os.path.basename(path)


def get_path_to_module(__file___):
  """Get the path to a module.

  @param __file___: The __file__ variable of the module.
  @type __file___: str

  @return: The path to the module.
  @rtype: str
  """

  return os.path.sep.join(__file___.split(os.path.sep)[:-1])


def join(*paths):
  """Join the paths using the system separator.

  @param paths: The paths to join.
  @type paths: tuple[str]

  @return: The joined paths.
  @rtype: str
  """

  paths = [i for i in paths if i]

  return os.path.sep.join(paths)


def read(path):
  """Read the contents of the file and return it as a string.

  @param path: The path of the file.
  @type path: str

  @return: The contents of the file.
  @rtype: str
  """

  with open(path, "r") as inf:
    return inf.read()


def split(path):
  """Split the path using the system separator.

  @param path: The paths to join.
  @type path: str

  @return: The split path.
  @rtype: list[str]
  """

  return path.split(os.path.sep)


def write(path, content):
  """Write the contents to the file.

  @param path: The paths of the file.
  @type path: str
  @param content: The content to write.
  @type content: str
  """

  with open(path, "w+") as out_f:
    out_f.write(content)
