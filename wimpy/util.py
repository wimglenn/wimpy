import os
from contextlib import contextmanager
from functools import update_wrapper

from wimpy.compat import zip_longest


__all__ = ['cached_property', 'working_directory', 'strip_prefix', 'strip_suffix', 'ceiling_division', 'grouper']


class cached_property(object):
    """
    non-data descriptor: property is computed once per instance and then replaces itself
    with an ordinary attribute.  Deleting the attribute invalidates the cache.
    """
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


@contextmanager
def working_directory(path):
    """Change working directory and restore the previous on exit"""
    prev_dir = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_dir)


def strip_prefix(s, prefix):
    """Removes the prefix, if it's there, otherwise returns input string unchanged"""
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def strip_suffix(s, suffix):
    """Removes the suffix, if it's there, otherwise returns input string unchanged"""
    if s.endswith(suffix):
        return s[:len(s) - len(suffix)]
    return s


def ceiling_division(numerator, denominator):
    """Divide and round up"""
    # Implementation relies on Python's // operator using floor division (round down)
    # This might surprise C users who expect rounding towards zero
    return -(-numerator//denominator)


def grouper(iterable, n, fillvalue=None):
    """Yield successive non-overlapping chunks of size n from iterable"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
