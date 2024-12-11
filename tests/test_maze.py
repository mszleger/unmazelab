import numpy as np
import pytest
import random

from app.maze import *

def test_size():
    m = Maze(np.array([2, 2]), 0)
    assert (m.size == np.array([2, 2])).all()
    with pytest.raises(ValueError, match="Size must be numpy.ndarray"):
        m.size = 5
    with pytest.raises(ValueError, match="Size must be one dimensional array with two values"):
        m.size = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Both values of size must be equal or greater than 2"):
        m.size = np.array([1, 2])

def test_seed():
    m = Maze(np.array([2, 2]), 0)
    assert m.seed == 0
    with pytest.raises(ValueError, match="Seed must be integer"):
        m.seed = "test"

def test_start_pos():
    m = Maze(np.array([2, 2]), 0)
    m.start_pos = np.array([0, 0])
    assert (m.start_pos == np.array([0, 0])).all()
    with pytest.raises(ValueError, match="Start position must be numpy.ndarray"):
        m.start_pos = 5
    with pytest.raises(ValueError, match="Start position must be one dimensional array with two values"):
        m.start_pos = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Start position is outside of the maze"):
        m.start_pos = np.array([1, 2])

def test_finish_pos():
    m = Maze(np.array([2, 2]), 0)
    m.finish_pos = np.array([0, 0])
    assert (m.finish_pos == np.array([0, 0])).all()
    with pytest.raises(ValueError, match="Finish position must be numpy.ndarray"):
        m.finish_pos = 5
    with pytest.raises(ValueError, match="Finish position must be one dimensional array with two values"):
        m.finish_pos = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Finish position is outside of the maze"):
        m.finish_pos = np.array([1, 2])

def test_load():
    m = Maze(np.array([2, 2]), 0)
    tree = ET.parse("tests/data/xml/maze.xml")
    root = tree.getroot()
    m.load(root)
    assert int(m.size[0]) == 10
    assert int(m.size[1]) == 20
    assert m.seed == 5

def test_save():
    m = Maze(np.array([6, 3]), 2)
    root = ET.Element("config")
    m.save(root)
    assert root.find("width").text == "3"
    assert root.find("height").text == "6"
    assert root.find("seed").text == "2"

def test_generate_start_pos():
    m = Maze(np.array([2, 2]), 0)
    random.seed(0)
    m.generate_start_pos()
    assert (m.start_pos == np.array([1, 1])).all()

def test_generate_finish_pos():
    m = Maze(np.array([2, 2]), 0)
    random.seed(0)
    m.generate_start_pos()
    m.generate_finish_pos()
    assert (m.finish_pos == np.array([0, 1])).all()

def test_if_start_and_finish_pos_not_equal():
    for seed in range(0, 1000):
        m = Maze(np.array([2, 2]), seed)
        m.generate()
        assert (m.start_pos != m.finish_pos).any()

def test_generate_walls():
    m = Maze(np.array([100, 100]), 0)
    random.seed(0)
    m.generate_walls()
    assert (m.vertical_walls == True).any()
    assert (m.vertical_walls != True).any()
    assert (m.horizontal_walls == True).any()
    assert (m.horizontal_walls != True).any()

def test_set_walls_everywhere():
    m = Maze(np.array([2, 2]), 0)
    m.set_walls_everywhere()
    assert m.vertical_walls.size == 2
    for value in np.nditer(m.vertical_walls):
        assert value == True
    assert m.horizontal_walls.size == 2
    for value in np.nditer(m.horizontal_walls):
        assert value == True

def test_remove_wall_between_neighbours():
    m = Maze(np.array([2, 2]), 0)
    m.set_walls_everywhere()
    m.remove_wall_between_neighbours(np.array([0, 0]), np.array([0, 1]))
    assert m.vertical_walls[0][0] == False
    m.set_walls_everywhere()
    m.remove_wall_between_neighbours(np.array([0, 0]), np.array([1, 0]))
    assert m.horizontal_walls[0][0] == False
    m.set_walls_everywhere()
    m.remove_wall_between_neighbours(np.array([1, 1]), np.array([0, 1]))
    assert m.horizontal_walls[0][1] == False
    m.set_walls_everywhere()
    m.remove_wall_between_neighbours(np.array([1, 1]), np.array([1, 0]))
    assert m.vertical_walls[1][0] == False

def test_get_frame_for_solver():
    m = Maze(np.array([2, 2]), 0)
    m.generate()
    assert m.get_frame_for_solver() == '2\n2\n1\n1\n0\n1\n0\n0\n1\n0\n'