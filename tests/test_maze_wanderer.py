from app.maze import Maze
from app.maze_wanderer import *

def test_default_constructor():
    m = Maze(2, 3, 0)
    mw = MazeWanderer(m)
    assert mw.maze is m
    assert (mw.grid == -1).all()
    assert mw.grid.size == 2 * 3
    assert mw.grid.shape[0] == 2
    assert mw.grid.shape[1] == 3

def test_get_grid_with_distanses_from_pos():
    m = Maze(2, 2, 0)
    m.vertical_walls = np.array([[True], [False]])
    m.horizontal_walls = np.array([[False, False]])
    mw = MazeWanderer(m)
    grid = mw.get_grid_with_distanses_from_pos(np.array([0, 0]))
    assert (grid == np.array([[0, 3], [1, 2]])).all()

def test_get_nonvisited_accessible_neighbours():
    m = Maze(2, 2, 0)
    m.vertical_walls = np.array([[True], [False]])
    m.horizontal_walls = np.array([[False, False]])
    mw = MazeWanderer(m)
    mw.grid[0][0] = 0
    assert (mw.get_nonvisited_accessible_neighbours(np.array([1, 0])) == np.array([[1, 1]])).all()

def test_get_all_accessible_neighbours():
    m = Maze(2, 2, 0)
    m.vertical_walls = np.array([[True], [False]])
    m.horizontal_walls = np.array([[False, False]])
    mw = MazeWanderer(m)
    assert (mw.get_all_accessible_neighbours(np.array([0, 0])) == np.array([[1, 0]])).all()
    assert (mw.get_all_accessible_neighbours(np.array([1, 0])) == np.array([[0, 0], [1, 1]])).all()
    assert (mw.get_all_accessible_neighbours(np.array([1, 1])) == np.array([[0, 1], [1, 0]])).all()
    assert (mw.get_all_accessible_neighbours(np.array([0, 1])) == np.array([[1, 1]])).all()

