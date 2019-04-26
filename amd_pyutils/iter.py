from itertools import groupby


def count(itr, key):
  """Count members of an iterable by dict key or grouping function.

  @param itr: The iterable containing items to count.
  @type itr: collections.abc.Iterable
  @param key: The string key or grouping function.
  @type key: str | function

  @return: A dict of item count by key.
  @rtype: dict
  """

  grouped = group(itr, key)

  return {k: len(v) for k, v in grouped.items()}


def first(itr):
  """Get the first value from an iterable or return None.

  @param itr: An iterable.
  @type itr: collections.abc.Iterable

  @return: The first item of the iterable, or None.
  @rtype: object | None
  """

  lst = list(itr)

  return lst[0] if lst else None


def group(itr, key):
  """Group an iterable by dict key or grouping function. Handles sorting and returns lists.

  @param itr: The iterable containing items to group.
  @type itr: collections.abc.Iterable
  @param key: The string key or grouping function.
  @type key: str | function

  @return: A dict of grouped items.
  @rtype: dict
  """

  res = {}
  key_func = (lambda i: i[key]) if not callable(key) else key
  sorted_itr = sorted(itr, key=key_func)
  for k, v in groupby(sorted_itr, key=key_func):
    res[k] = list(v)

  return res


def index(itr, idx):
  """Get the value from the index of an iterable or return None.

  @param itr: An iterable.
  @type itr: collections.abc.Iterable
  @param idx: The index to get.
  @type idx: int

  @return: The item at the specified index of the iterable, or None.
  @rtype: object | None
  """

  lst = list(itr)

  return lst[idx] if lst and len(lst) > abs(idx) else None


def last(itr):
  """Get the last value from an iterable or return None.

  @param itr: An iterable.
  @type itr: collections.abc.Iterable

  @return: The last item of the iterable, or None.
  @rtype: object | None
  """

  return index(itr, -1)


def single(itr):
  """Get a single value from an iterable or return None, erroring if there is more than one value.

  @param itr: An iterable.
  @type itr: collections.abc.Iterable

  @return: The only item in the iterable.
  @rtype: object | None
  """

  lst = list(itr)
  if lst:
    if len(lst) > 1:
      raise ValueError("More than one value in iterable")
    return lst[0]

  return None


def take(itr, n):
  """Take n values from an iterable.

  A number greater than the length of the iterable will return the whole iterable.

  @param itr: An iterable.
  @type itr: collections.abc.Iterable
  @param n: The number of items to take.
  @type n: int

  @return: A list of items from the iterable.
  @rtype: list[object]
  """

  lst = list(itr)
  if lst:
    return [lst[i] for i in range(n) if i < len(lst)]

  return []
