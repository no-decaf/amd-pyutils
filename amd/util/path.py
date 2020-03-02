"""Functions for working with os.path."""

import os


def ensure(path: str) -> None:
    """Ensure the path exists.

    :param path: The path to ensure.
    """

    if not os.path.exists(path):
        os.makedirs(path)


def get_module_path(__file___: str) -> str:
    """Get the path to a module.

    :param __file___: The __file__ value of the module.

    :return: The path to the module.
    """

    return os.path.dirname(os.path.abspath(__file___))
