import random
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from app.maze import Maze
from app.solver import Solver

class MazeVisualizerTab:
    def __init__(self, window, app_state):
        self.app_state = app_state
        self.set_references_to_ui_elements(window)
        self.connect_signals()
        self.update_main_maze_ui()

    def set_references_to_ui_elements(self, window):
        self.status_bar      = window.statusbar
        self.canvas          = window.maze_tab_canvas
        self.list_of_solvers = window.maze_tab_solver_selector
        self.maze_width      = window.maze_tab_generator_width
        self.maze_height     = window.maze_tab_generator_height
        self.maze_seed       = window.maze_tab_generator_seed
        self.btn_random_seed = window.maze_tab_generator_btn_random
        self.btn_generate    = window.maze_tab_generator_btn_generate
        self.btn_solve       = window.maze_tab_solver_btn_solve

    def connect_signals(self):
        self.maze_height.textChanged.connect(self.save_height)
        self.maze_width.textChanged.connect(self.save_width)
        self.maze_seed.textChanged.connect(self.save_seed)
        self.btn_random_seed.clicked.connect(lambda: self.maze_seed.setText(str(random.randint(0,999999))))
        self.btn_generate.clicked.connect(self.generate_maze)
        self.btn_solve.clicked.connect(self.solve_maze)

    def generate_maze(self):
        self.app_state.main_maze.generate()
        self.draw_maze()

    def solve_maze(self):
        self.generate_maze()
        solver = self.app_state.solver_list[self.list_of_solvers.currentIndex()]
        solution = solver.run(self.app_state.main_maze)
        self.draw_solution(solution)

    def save_height(self):
        self.app_state.main_maze.size[0] = int(self.maze_height.text())
        self.app_state.save()

    def save_width(self):
        self.app_state.main_maze.size[1] = int(self.maze_width.text())
        self.app_state.save()

    def save_seed(self):
        self.app_state.main_maze.seed = int(self.maze_seed.text())
        self.app_state.save()

    def update_main_maze_ui(self):
        self.maze_height.setText(str(self.app_state.main_maze.size[0]))
        self.maze_width.setText(str(self.app_state.main_maze.size[1]))
        self.maze_seed.setText(str(self.app_state.main_maze.seed))

    def draw_maze(self):
        pass

    def draw_solution(self, solution):
        pass
