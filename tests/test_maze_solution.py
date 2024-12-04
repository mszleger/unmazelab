from app.maze_solution import *
import numpy as np

def test_get_solver_name():
    ms = MazeSolution("DummySolver")
    assert ms.get_solver_name() == "DummySolver"

def test_load_solution_from_solver():
    ms = MazeSolution("DummySolver")
    ms.load_solution_from_solver("1000\n1\n2\n3\n4\n")
    assert ms.get_solving_time() == 1000
    assert (ms.get_path() == np.array([[1, 2], [3, 4]])).all()