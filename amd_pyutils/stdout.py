import sys


def write(output):
  """Write the output to STDOUT and flush STDOUT.

  @param output: The output to print.
  @type output: str
  """
  sys.stdout.write(output)
  sys.stdout.flush()
