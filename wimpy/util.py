import os
from collections import deque
from contextlib import contextmanager
from functools import update_wrapper

from wimpy.compat import range
from wimpy.compat import zip_longest
from wimpy.exceptions import WimpyError


__all__ = [
    "cached_property",
    "working_directory",
    "strip_prefix",
    "strip_suffix",
    "ceiling_division",
    "grouper",
    "chunks",
    "is_subsequence",
]


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


def strip_prefix(s, prefix, strict=False):
    """Removes the prefix, if it's there, otherwise returns input string unchanged.
    If strict is True, also ensures the prefix was present"""
    if s.startswith(prefix):
        return s[len(prefix) :]
    elif strict:
        raise WimpyError("string doesn't start with prefix")
    return s


def strip_suffix(s, suffix, strict=False):
    """Removes the suffix, if it's there, otherwise returns input string unchanged.
    If strict is True, also ensures the suffix was present"""
    if s.endswith(suffix):
        return s[: len(s) - len(suffix)]
    elif strict:
        raise WimpyError("string doesn't end with suffix")
    return s


def ceiling_division(numerator, denominator):
    """Divide and round up"""
    # Implementation relies on Python's // operator using floor division (round down)
    # This might surprise C users who expect rounding towards zero
    return -(-numerator // denominator)


def grouper(iterable, n, fillvalue=None):
    """Yield successive non-overlapping chunks of size n from iterable"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def chunks(iterable, chunk_size=3, overlap=0):
    # we'll use a deque to hold the values because it automatically
    # discards any extraneous elements if it grows too large
    if chunk_size < 1:
        raise WimpyError("chunk size too small")
    if overlap >= chunk_size:
        raise WimpyError("overlap too large")
    queue = deque(maxlen=chunk_size)
    it = iter(iterable)
    i = 0
    try:
        # start by filling the queue with the first group
        for i in range(chunk_size):
            queue.append(next(it))
        while True:
            yield tuple(queue)
            # after yielding a chunk, get enough elements for the next chunk
            for i in range(chunk_size - overlap):
                queue.append(next(it))
    except StopIteration:
        # if the iterator is exhausted, yield any remaining elements
        i += overlap
        if i > 0:
            yield tuple(queue)[-i:]


def is_subsequence(needle, haystack):
    """Are all the elements of needle contained in haystack, and in the same order?
    There may be other elements interspersed throughout"""
    it = iter(haystack)
    for element in needle:
        if element not in it:
            return False
    return True
