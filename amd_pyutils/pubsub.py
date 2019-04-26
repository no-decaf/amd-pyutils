"""Functions for publishing and subscribing to topics with no external dependencies."""

from collections import defaultdict
from copy import deepcopy

subscribers = defaultdict(list)


def publish(topic, obj):
  """Publish an object as a JSON-formatted message to a Google Cloud Pub/Sub topic.

  @param topic: The name of the topic.
  @type topic: str
  @param obj: An object that can be serialized to JSON.
  @type obj: object
  """

  for subscriber in subscribers.get(topic, []):
    subscriber(deepcopy(obj))


def subscribe(topic, func):
  """Subscribe to a topic.

  @param topic: The name of the topic.
  @type topic: str
  @param func: The function to call when a message is published to the topic.
  @type func: function
  """

  subscribers[topic].append(func)
