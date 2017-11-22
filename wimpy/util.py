import os
from contextlib import contextmanager
from functools import update_wrapper


__all__ = ['cached_property', 'working_directory', 'strip_prefix', 'strip_suffix']


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
