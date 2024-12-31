import numpy as np
import pytest
import xml.etree.ElementTree as ET

from app.maze import Maze
from app.solver import *

def test_default_constructor():
    s = Solver("Solver Name", "Solver Command", True)
    assert s.name == "Solver Name"
    assert s.command == "Solver Command"
    assert s.checked == True

def test_xml_loading_constructor():
    tree = ET.parse("tests/data/xml/solver.xml")
    root = tree.getroot()
    s = Solver(root)
    assert s.name == "Solver Name"
    assert s.command == "Solver Command"
    assert s.checked == True

def test_name():
    s = Solver("Solver Name", "Solver Command", True)
    s.name = "Solver Name 2"
    assert s.name == "Solver Name 2"
    with pytest.raises(ValueError, match="Name must be string"):
        s.name = 5
    with pytest.raises(ValueError, match="Name can't be empty string"):
        s.name = ""

def test_command():
    s = Solver("Solver Name", "Solver Command", True)
    s.command = "Solver Command 2"
    assert s.command == "Solver Command 2"
    with pytest.raises(ValueError, match="Command must be string"):
        s.command = 5
    with pytest.raises(ValueError, match="Command can't be empty string"):
        s.command = ""

def test_checked():
    s = Solver("Solver Name", "Solver Command", True)
    s.checked = False
    assert s.checked == False
    with pytest.raises(ValueError, match="Checked must be boolean"):
        s.checked = 5

def test_load():
    s = Solver("Default", "Default", False)
    tree = ET.parse("tests/data/xml/solver.xml")
    root = tree.getroot()
    s.load(root)
    assert s.name == "Solver Name"
    assert s.command == "Solver Command"
    assert s.checked == True

def test_save():
    s = Solver("Solver Name", "Solver Command", True)
    root = ET.Element("config")
    s.save(root)
    assert root.find("name").text == "Solver Name"
    assert root.find("command").text == "Solver Command"
    assert root.find("checked").text == "True"

def test_run():
    m = Maze(2, 2, 0)
    m.generate()
    s = Solver("DummySolver", "python tests/scripts/dummy_solver.py", False)
    maze_solution = s.run(m)
    assert maze_solution.solving_time_us == 1000
    assert (maze_solution.path == np.array([[1, 2], [3, 4]])).all()