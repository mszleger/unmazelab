from app.maze import Maze
from app.maze_solution import MazeSolution
from app.solver import *
import numpy as np

def test_run_solver():
    m = Maze(np.array([2, 2]), 0)
    s = Solver("DummySolver", "python tests/data/solver/dummy_solver.py")
    solution = s.run(m)
    assert solution.get_solver_name() == s.get_name()
    assert solution.get_solving_time() == 1000
    assert (solution.get_path() == np.array([[1, 2], [3, 4]])).all()