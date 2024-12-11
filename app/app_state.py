import numpy as np
import os
import xml.etree.ElementTree as ET

from app.maze import Maze
from app.solver import Solver

class AppState:
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path):
            self.load()
            print(f"Loaded configuration from {self.file_path} file")
        else:
            self.set_default_params()
            self.save()
            print("Loading configuration from file failed")
            print("Loaded default parameters")

    def load(self):
        self.main_maze = Maze(np.array([10, 20]), 999)
        self.solver_list = []
        self.maze_list = []
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for section in root:
            if section.tag == "visualized_maze_param":
                self.load_main_maze(section)
            elif section.tag == "solver_list":
                self.load_solvers(section)
            elif section.tag == "testing_maze_param_list":
                self.load_mazes(section)

    def save(self):
        root = ET.Element("config")
        main_maze_root   = ET.SubElement(root, "main_maze")
        solver_list_root = ET.SubElement(root, "solver_list")
        maze_list_root   = ET.SubElement(root, "maze_list")
        self.save_main_maze(main_maze_root)
        self.save_solvers(solver_list_root)
        self.save_mazes(maze_list_root)
        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def set_default_params(self):
        self.main_maze = Maze(np.array([10, 20]), 999)
        self.solver_list = []
        self.maze_list = []

    def load_main_maze(self, main_maze_root):
        self.main_maze = Maze(main_maze_root)

    def save_main_maze(self, main_maze_root):
        self.main_maze.save(main_maze_root)

    def load_solvers(self, solver_list_root):
        for solver in solver_list_root:
            self.solver_list.append(Solver(solver))

    def save_solvers(self, solver_list_root):
        for solver in self.solver_list:
            solver_root = ET.SubElement(solver_list_root, "solver")
            solver.save(solver_root)

    def load_mazes(self, maze_list_root):
        for maze in maze_list_root:
            self.maze_list.append(Maze(maze))

    def save_mazes(self, maze_list_root):
        for maze in self.maze_list:
            maze_root = ET.SubElement(maze_list_root, "maze_param")
            maze.save(maze_root)