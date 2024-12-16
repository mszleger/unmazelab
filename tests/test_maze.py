import numpy as np
import pytest

from app.maze import *
from app.maze_wanderer import MazeWanderer

def test_default_constructor():
    m = Maze(2, 3, 0)
    assert (m.size == np.array([2, 3])).all()
    assert m.seed == 0

def test_numpy_array_constructor():
    m = Maze(np.array([2, 3]), 0)
    assert (m.size == np.array([2, 3])).all()
    assert m.seed == 0

def test_xml_loading_constructor():
    tree = ET.parse("tests/data/xml/maze.xml")
    root = tree.getroot()
    m = Maze(root)
    assert int(m.size[0]) == 10
    assert int(m.size[1]) == 20
    assert m.seed == 5

def test_size():
    m = Maze(2, 2, 0)
    m.generate()
    m.size = np.array([3, 4])
    assert (m.size == np.array([3, 4])).all()
    assert m.vertical_walls == None
    assert m.horizontal_walls == None
    assert m.start_pos == None
    assert m.finish_pos == None
    with pytest.raises(ValueError, match="Size must be numpy.ndarray"):
        m.size = 5
    with pytest.raises(ValueError, match="Size must be one dimensional array with two values"):
        m.size = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Both values of size must be equal or greater than 2"):
        m.size = np.array([1, 2])

def test_seed():
    m = Maze(2, 2, 0)
    m.seed = 1
    assert m.seed == 1
    with pytest.raises(ValueError, match="Seed must be integer"):
        m.seed = "test"

def test_start_pos():
    m = Maze(2, 2, 0)
    m.start_pos = np.array([0, 1])
    assert (m.start_pos == np.array([0, 1])).all()
    with pytest.raises(ValueError, match="Start position must be numpy.ndarray"):
        m.start_pos = 5
    with pytest.raises(ValueError, match="Start position must be one dimensional array with two values"):
        m.start_pos = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Start position is outside of the maze"):
        m.start_pos = np.array([1, 2])

def test_finish_pos():
    m = Maze(2, 2, 0)
    m.finish_pos = np.array([0, 1])
    assert (m.finish_pos == np.array([0, 1])).all()
    with pytest.raises(ValueError, match="Finish position must be numpy.ndarray"):
        m.finish_pos = 5
    with pytest.raises(ValueError, match="Finish position must be one dimensional array with two values"):
        m.finish_pos = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Finish position is outside of the maze"):
        m.finish_pos = np.array([1, 2])

def test_load():
    m = Maze(2, 2, 0)
    tree = ET.parse("tests/data/xml/maze.xml")
    root = tree.getroot()
    m.load(root)
    assert int(m.size[0]) == 10
    assert int(m.size[1]) == 20
    assert m.seed == 5

def test_save():
    m = Maze(6, 3, 2)
    root = ET.Element("config")
    m.save(root)
    assert root.find("height").text == "6"
    assert root.find("width").text == "3"
    assert root.find("seed").text == "2"

def test_generate_start_pos_higher():
    m = Maze(10, 5, 0)
    m.generate()
    assert type(m.start_pos) != type(None)

def test_generate_start_pos_wider():
    m = Maze(5, 10, 0)
    m.generate()
    assert type(m.start_pos) != type(None)

def test_generate_finish_pos_higher():
    m = Maze(10, 5, 0)
    m.generate()
    assert type(m.generate_finish_pos) != type(None)

def test_generate_finish_pos_wider():
    m = Maze(5, 10, 0)
    m.generate()
    assert type(m.generate_finish_pos) != type(None)

def test_if_start_and_finish_pos_are_possibly_furthest_away():
    for seed in range(0, 100):
        m = Maze(10, 10, seed)
        m.generate()
        mw = MazeWanderer(m)
        g = mw.get_grid_with_distanses_from_pos(m.start_pos)
        finish_dist = g[m.finish_pos[0]][m.finish_pos[1]]
        assert g.max() == finish_dist

def test_generate_walls():
    m = Maze(10, 10, 0)
    m.generate_walls()
    assert (m.vertical_walls == True).any()
    assert (m.vertical_walls != True).any()
    assert (m.horizontal_walls == True).any()
    assert (m.horizontal_walls != True).any()

def test_generate_walls_if_all_cells_are_connected():
    for seed in range(0, 100):
        m = Maze(10, 10, seed)
        m.generate()
        mw = MazeWanderer(m)
        g = mw.get_grid_with_distanses_from_pos(np.array([0, 0]))
        assert (g != -1).all()

def test_set_walls_everywhere():
    m = Maze(2, 2, 0)
    m.set_walls_everywhere()
    assert m.vertical_walls.size == 2
    assert m.vertical_walls.shape[0] == m.size[0]
    assert m.vertical_walls.shape[1] == m.size[1] - 1
    assert (m.vertical_walls == True).all()
    assert m.horizontal_walls.size == 2
    assert m.horizontal_walls.shape[0] == m.size[0] - 1
    assert m.horizontal_walls.shape[1] == m.size[1]
    assert (m.horizontal_walls == True).all()

def test_remove_wall_between_neighbours():
    m = Maze(2, 2, 0)
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
    m = Maze(2, 2, 0)
    m.generate()
    frame  = f'{m.size[0]}\n{m.size[1]}\n'
    frame += f'{m.start_pos[0]}\n{m.start_pos[1]}\n'
    frame += f'{m.finish_pos[0]}\n{m.finish_pos[1]}\n'
    frame += f'{int(m.vertical_walls[0][0])}\n{int(m.vertical_walls[1][0])}\n'
    frame += f'{int(m.horizontal_walls[0][0])}\n{int(m.horizontal_walls[0][1])}\n'
    assert m.get_frame_for_solver() == frame