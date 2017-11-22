import os
from random import random

import pytest

from wimpy.util import cached_property
from wimpy.util import strip_prefix
from wimpy.util import strip_suffix
from wimpy.util import working_directory


@pytest.mark.parametrize('in_,pre,out', [
    ('www.yahoo.com', 'www.', 'yahoo.com'),
    ('www.yahoo.com', 'Www.', 'www.yahoo.com'),
])
def test_strip_prefix(in_, pre, out):
    assert strip_prefix(in_, pre) == out


@pytest.mark.parametrize('in_,suf,out', [
    ('www.yahoo.com', 'www.', 'www.yahoo.com'),
    ('www.yahoo.com', '.com', 'www.yahoo'),
])
def test_strip_suffix(in_, suf, out):
    assert strip_suffix(in_, suf) == out


def test_working_directory(tmpdir):
    before = os.getcwd()
    with working_directory(tmpdir):
        inside = os.getcwd()
    after = os.getcwd()
    assert before == after != inside


class A:
    @cached_property
    def prop(self):
        return random()


def test_cached_property():
    a = A()
    assert 'prop' not in a.__dict__
    x = a.prop
    assert 'prop' in a.__dict__
    y = a.prop
    assert 0. < x == y < 1.
    del a.prop  # invalidate cache
    z = a.prop  # prop recomputed
    assert x == y != z
    del a.prop  # this deletes from instance dict
    with pytest.raises(AttributeError):
        del a.prop  # .. but you can't delete the descriptor
    assert isinstance(a.prop, float)
    assert isinstance(A.prop, cached_property)
