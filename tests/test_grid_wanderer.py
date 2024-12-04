from app.grid_wanderer import *
import numpy as np

def test_pos_set_get():
    gw = GridWanderer(np.array([5, 5]))
    gw.set_current_pos(np.array([3, 2]))
    assert (gw.get_current_pos() == np.array([3, 2])).all()
    gw.set_current_pos(np.array([4, 1]))
    assert (gw.get_current_pos() == np.array([4, 1])).all()

def test_get_all_neighbours_middle():
    gw = GridWanderer(np.array([5, 5]))
    gw.set_current_pos(np.array([2, 2]))
    assert (gw.get_all_neighbours() == np.array([[1, 2], [3, 2],[2, 1], [2, 3]])).all()

def test_get_all_neighbours_top_left_corner():
    gw = GridWanderer(np.array([5, 5]))
    gw.set_current_pos(np.array([0, 0]))
    assert (gw.get_all_neighbours() == np.array([[1, 0], [0, 1]])).all()

def test_get_all_neighbours_bottom_right_corner():
    gw = GridWanderer(np.array([5, 5]))
    gw.set_current_pos(np.array([4, 4]))
    assert (gw.get_all_neighbours() == np.array([[3, 4], [4, 3]])).all()

def test_get_unvisited_neighbours():
    gw = GridWanderer(np.array([5, 5]))
    gw.set_current_pos(np.array([1, 2]))
    gw.set_current_pos(np.array([2, 1]))
    gw.set_current_pos(np.array([2, 2]))
    assert (gw.get_unvisited_neighbours() == np.array([[3, 2], [2, 3]])).all()