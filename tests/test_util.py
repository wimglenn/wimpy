import os
from random import random

import pytest

from wimpy import cached_property
from wimpy import ceiling_division
from wimpy import chunks
from wimpy import grouper
from wimpy import strip_prefix
from wimpy import strip_suffix
from wimpy import WimpyError
from wimpy import working_directory


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


@pytest.mark.parametrize('numerator,denominator,result', [
    (51, 10, 6),
    (50, 10, 5),
    (49, 10, 5),
    (-49, 10, -4),
])
def test_ceiling_div(numerator, denominator, result):
    assert ceiling_division(numerator, denominator) == result



@pytest.mark.parametrize('iterable,n,fillvalue,result', [
    (range(6), 2, None, [(0, 1), (2, 3), (4, 5)]),
    (range(5), 2, None, [(0, 1), (2, 3), (4, None)]),
    (range(5), 2, 123, [(0, 1), (2, 3), (4, 123)]),
])
def test_grouper(iterable, n, fillvalue, result):
    assert list(grouper(iterable, n, fillvalue)) == result


@pytest.mark.parametrize('iterable,chunk_size,overlap,result', [
    ('1234567', 3, 0, [['1', '2', '3'], ['4', '5', '6'], ['7']]),
    ('123456', 3, 0, [['1', '2', '3'], ['4', '5', '6']]),
    ('123456', 4, 2, [['1', '2', '3', '4'], ['3', '4', '5', '6']]),
    ('', 3, 0, []),
])
def test_chunks(iterable, chunk_size, overlap, result):
    assert list(chunks(iterable, chunk_size, overlap)) == result


def test_chunks_doesnt_get_stuck_due_to_small_chunk_size():
    gen = chunks('123456', chunk_size=0)
    with pytest.raises(WimpyError, match='chunk size too small'):
        next(gen)


def test_chunks_doesnt_get_stuck_due_to_big_overlap():
    gen = chunks('123456', chunk_size=3, overlap=3)
    with pytest.raises(WimpyError, match='overlap too large'):
        next(gen)


def test_chunks_from_infinite_generator():
    gen = iter(int, 1)
    g = chunks(gen, chunk_size=5)
    assert next(g) == [0, 0, 0, 0, 0]
    assert next(g) == [0, 0, 0, 0, 0]
    assert next(g) == [0, 0, 0, 0, 0]
