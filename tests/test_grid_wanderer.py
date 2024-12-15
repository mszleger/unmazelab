import numpy as np
import pytest

from app.grid_wanderer import *

def test_default_constructor():
    gw = GridWanderer(np.array([5, 5]))
    assert (gw.size == np.array([5, 5])).all()

def test_size():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([0, 0])
    gw.size = np.array([6, 4])
    assert (gw.size == np.array([6, 4])).all()
    assert gw._current_pos == None
    with pytest.raises(ValueError, match="Size must be numpy.ndarray"):
        gw.size = 5
    with pytest.raises(ValueError, match="Size must be one dimensional array with two values"):
        gw.size = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Both values of size must be equal or greater than 2"):
        gw.size = np.array([1, 2])

def test_current_pos():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([0, 1])
    assert (gw.size == np.array([0, 1])).all()
    with pytest.raises(ValueError, match="Current position must be numpy.ndarray"):
        gw.current_pos = 5
    with pytest.raises(ValueError, match="Current position must be one dimensional array with two values"):
        gw.current_pos = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Current position is outside of the grid"):
        gw.current_pos = np.array([-1, 5])

def test_get_all_neighbours_middle():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([2, 2])
    assert (gw.get_all_neighbours() == np.array([[1, 2], [3, 2],[2, 1], [2, 3]])).all()

def test_get_all_neighbours_top_left_corner():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([0, 0])
    assert (gw.get_all_neighbours() == np.array([[1, 0], [0, 1]])).all()

def test_get_all_neighbours_bottom_right_corner():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([4, 4])
    assert (gw.get_all_neighbours() == np.array([[3, 4], [4, 3]])).all()

def test_get_unvisited_neighbours():
    gw = GridWanderer(np.array([5, 5]))
    gw.current_pos = np.array([1, 2])
    gw.current_pos = np.array([2, 1])
    gw.current_pos = np.array([2, 2])
    assert (gw.get_unvisited_neighbours() == np.array([[3, 2], [2, 3]])).all()