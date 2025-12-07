#!/usr/bin/env python3
"""
Utility functions for testing: access_nested_map, get_json, and memoize decorator.
"""

from typing import Any, Dict, Tuple, Callable
import requests
from functools import wraps


def access_nested_map(nested_map: Dict, path: Tuple) -> Any:
    """
    Access a nested map and return the value at the specified path.

    Args:
        nested_map (dict): Dictionary to traverse.
        path (tuple): Tuple of keys representing the path.

    Returns:
        Any: Value found at the end of the path.

    Raises:
        KeyError: If any key in path is missing.
    """
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Dict:
    """
    Make an HTTP GET request and return JSON response.

    Args:
        url (str): URL to request.

    Returns:
        dict: JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> property:
    """
    Decorator to cache the result of a method as a property.

    Returns:
        property: Cached result as a read-only property.
    """
    attr_name = "_cached_" + fn.__name__

    @property
    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return wrapper
