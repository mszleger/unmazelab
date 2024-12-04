from app.maze import *
import numpy as np
import random

def test_get_size():
    m = Maze(np.array([2, 2]), 0)
    size = m.get_size()
    size[0] = 3
    assert (m.get_size() == np.array([2, 2])).all()

def test_get_start_pos():
    m = Maze(np.array([2, 2]), 0)
    pos = m.get_start_pos()
    pos_copy = pos.copy()
    pos[0] = 3
    assert (m.get_start_pos() == pos_copy).all()

def test_get_finish_pos():
    m = Maze(np.array([2, 2]), 0)
    pos = m.get_finish_pos()
    pos_copy = pos.copy()
    pos[0] = 3
    assert (m.get_finish_pos() == pos_copy).all()

def test_if_start_and_finish_pos_not_equal():
    for seed in range(0, 1000):
        m = Maze(np.array([2, 2]), seed)
        assert (m.get_start_pos() != m.get_finish_pos()).any()

def test_get_vertical_walls():
    m = Maze(np.array([2, 2]), 0)
    walls = m.get_vertical_walls()
    walls_copy = walls.copy()
    walls[0][0] = not walls[0][0]
    assert (m.get_vertical_walls() == walls_copy).all()

def test_get_horizontal_walls():
    m = Maze(np.array([2, 2]), 0)
    walls = m.get_horizontal_walls()
    walls_copy = walls.copy()
    walls[0][0] = not walls[0][0]
    assert (m.get_horizontal_walls() == walls_copy).all()

def test_get_frame_for_solver():
    m = Maze(np.array([2, 2]), 0)
    assert m.get_frame_for_solver() == '2\n2\n1\n1\n0\n1\n0\n0\n1\n0\n'