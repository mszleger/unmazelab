from app.list_of_solvers import *
from app.maze import Maze
from app.maze_solution import MazeSolution
from app.solver import Solver
import numpy as np

def test_add():
    los = ListOfSovers()
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.add(s1)
    assert los.get(0).get_name() == s0.get_name()
    assert los.get(0).get_command() == s0.get_command()
    assert los.get(1).get_name() == s1.get_name()
    assert los.get(1).get_command() == s1.get_command()

def test_edit():
    los = ListOfSovers()
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.edit(0, s1)
    assert los.get(0).get_name() == s1.get_name()
    assert los.get(0).get_command() == s1.get_command()

def test_remove():
    los = ListOfSovers()
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.add(s1)
    los.remove(0)
    assert los.get(0).get_name() == s1.get_name()
    assert los.get(0).get_command() == s1.get_command()

def test_switch_places():
    los = ListOfSovers()
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.add(s1)
    los.switch_places(0, 1)
    assert los.get(1).get_name() == s0.get_name()
    assert los.get(1).get_command() == s0.get_command()
    assert los.get(0).get_name() == s1.get_name()
    assert los.get(0).get_command() == s1.get_command()

def test_run():
    los = ListOfSovers()
    m = Maze(np.array([2, 2]), 0)
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.add(s1)
    output = los.run([0, 1], m)
    assert output[0].get_solver_name() == "DummySolver0"
    assert output[1].get_solver_name() == "DummySolver1"

def test_run_changed_solvers_order():
    los = ListOfSovers()
    m = Maze(np.array([2, 2]), 0)
    s0 = Solver("DummySolver0", "python tests/data/solver/dummy_solver.py")
    s1 = Solver("DummySolver1", "python tests/data/solver/dummy_solver.py arg1")
    los.add(s0)
    los.add(s1)
    output = los.run([1, 0], m)
    assert output[0].get_solver_name() == "DummySolver1"
    assert output[1].get_solver_name() == "DummySolver0"