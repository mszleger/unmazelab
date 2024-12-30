import numpy as np
import pytest

from app.maze_solution import *

def test_default_constructor():
    ms = MazeSolution(1000, np.array([[1, 2], [3, 4]]))
    assert ms.solving_time_us == 1000
    assert (ms.path == np.array([[1, 2], [3, 4]])).all()

def test_frame_loading_constructor():
    ms = MazeSolution("1000\n1\n2\n3\n4\n")
    assert ms.solving_time_us == 1000
    assert (ms.path == np.array([[1, 2], [3, 4]])).all()

def test_solving_time_us():
    ms = MazeSolution(1000, np.array([[1, 2], [3, 4]]))
    ms.solving_time_us = 900
    assert ms.solving_time_us == 900
    with pytest.raises(ValueError, match="Solving time must be integer"):
        ms.solving_time_us = "test"

def test_path():
    ms = MazeSolution(1000, np.array([[1, 2], [3, 4]]))
    ms.path = np.array([[2, 3], [4, 5]])
    assert (ms.path == np.array([[2, 3], [4, 5]])).all()
    with pytest.raises(ValueError, match="Path must be numpy.ndarray"):
        ms.path = 5
    with pytest.raises(ValueError, match="Path must have two columns"):
        ms.path = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="Path must have at least two rows"):
        ms.path = np.array([[1, 2]])

def test_load_solver_output_frame():
    ms = MazeSolution("1000\n1\n2\n3\n4\n")
    assert ms.solving_time_us == 1000
    assert (ms.path == np.array([[1, 2], [3, 4]])).all()

def test_load_solver_output_frame_with_extra_whitespace_characters():
    ms = MazeSolution("\n \n 1000 \n \n 1 \n \n 2 \n\n 3 \n\n 4 \n\n")
    assert ms.solving_time_us == 1000
    assert (ms.path == np.array([[1, 2], [3, 4]])).all()