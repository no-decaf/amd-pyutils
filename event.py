from collections import defaultdict
from copy import deepcopy

subscribers = defaultdict(set)


def publish(name, data):
  for subscriber in subscribers[name]:
    subscriber(deepcopy(data))


def subscribe(name, method):
  subscribers[name].add(method)
