# No new info for docstring, so pylint: disable=missing-module-docstring

import pytest

from app import vector

def test_vector_2d_setter_and_getter():
    '''Tests setters and getters of class Vector2D.

    Checks if once set value is properly returned later and if type check
    of values to be set is working.
    '''
    vect = vector.Vector2D(2, 4)
    assert vect.x == 2
    assert vect.y == 4
    with pytest.raises(ValueError, match='X has to be value of type int'):
        vect.x = '2'
    with pytest.raises(ValueError, match='Y has to be value of type int'):
        vect.y = '4'

def test_vector_2d_repr_function():
    '''Tests string representation of class Vector2D.'''
    vect = vector.Vector2D(2, 4)
    assert repr(vect) == '(2, 4)'
