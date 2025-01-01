'''Module creating GUI for UnMazeLab application.

Module loads ui layout from file app/ui/main_window.ui and renders it. Apart
from MainWindow class module contains helper classes providing ui events
handlers.

Typical usage example:

  state = app_state.AppState()
  main_window = ui.MainWindow(state)
'''

import csv
import numpy as np
import random
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtUiTools
from PySide6 import QtWidgets

from app import app_state
from app import maze
from app import solver


class MainWindow:
    '''Main window of application.

    '''
    def __init__(self, state: app_state.AppState):
        self.state = state
        self.app = QtWidgets.QApplication(sys.argv)
        self.load_ui('app/ui/main_window.ui')
        self.connect_signals()
        self.window.show()
        sys.exit(self.app.exec())

    def load_ui(self, file_name):
        ui_file = QtCore.QFile(file_name)
        if not ui_file.open(QtCore.QIODevice.ReadOnly):
            print(f'Cannot open {file_name}: {ui_file.errorString()}')
            sys.exit(-1)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        if not self.window:
            print(loader.errorString())
            sys.exit(-1)

    def connect_signals(self):
        self.maze_visualizer_ui = MazeVisualizerTab(self.window, self.state)
        self.raport_generator_ui = RaportGeneratorTab(self.window, self.state)
        self.solvers_ui = SolversUI(self.window, self.state)


class MazeVisualizerTab:
    def __init__(self, window, state):
        self.state = state
        self.set_references_to_ui_elements(window)
        self.connect_signals()
        self.update_main_maze_ui()
        self.maze_painter = MazePainter(self.canvas)

    def set_references_to_ui_elements(self, window):
        self.status_bar      = window.statusbar
        self.canvas          = window.maze_tab_canvas
        self.list_of_solvers = window.maze_tab_solver_selector
        self.width      = window.maze_tab_generator_width
        self.height     = window.maze_tab_generator_height
        self.seed       = window.maze_tab_generator_seed
        self.btn_rand_seed = window.maze_tab_generator_btn_random
        self.btn_generate    = window.maze_tab_generator_btn_generate
        self.btn_solve       = window.maze_tab_solver_btn_solve

    def connect_signals(self):
        self.height.textChanged.connect(self.save_height)
        self.width.textChanged.connect(self.save_width)
        self.seed.textChanged.connect(self.save_seed)
        self.btn_rand_seed.clicked.connect(lambda: self.seed.setText(str(random.randint(0,999999))))
        self.btn_generate.clicked.connect(self.generate_maze)
        self.btn_solve.clicked.connect(self.solve_maze)

    def generate_maze(self):
        self.state.main_maze.generate()
        self.maze_painter.paint_maze(self.state.main_maze)

    def solve_maze(self):
        self.generate_maze()
        s = self.state.solver_list[self.list_of_solvers.currentIndex()]
        solution = s.run(self.state.main_maze)
        self.maze_painter.paint_solution(solution)

    def save_height(self):
        self.state.main_maze.size[0] = int(self.height.text())
        self.state.save()

    def save_width(self):
        self.state.main_maze.size[1] = int(self.width.text())
        self.state.save()

    def save_seed(self):
        self.state.main_maze.seed = int(self.seed.text())
        self.state.save()

    def update_main_maze_ui(self):
        self.height.setText(str(self.state.main_maze.size[0]))
        self.width.setText(str(self.state.main_maze.size[1]))
        self.seed.setText(str(self.state.main_maze.seed))


class RaportGeneratorTab:
    def __init__(self, window, state):
        self.state = state
        self.set_constants()
        self.set_references_to_ui_elements(window)
        self.connect_signals()
        self.update_maze_list_ui()

    def set_constants(self):
        self.col_width  = 0
        self.col_height = 1
        self.col_seed   = 2

    def set_references_to_ui_elements(self, window):
        self.table               = window.generator_tab_seeds_list
        self.lst_width           = window.generator_tab_seed_edit_width
        self.lst_height          = window.generator_tab_seed_edit_height
        self.lst_seed            = window.generator_tab_seed_edit_seed
        self.lst_btn_add         = window.generator_tab_seed_edit_btn_add
        self.lst_btn_edit        = window.generator_tab_seed_edit_btn_edit
        self.lst_btn_remove      = window.generator_tab_seed_edit_btn_remove
        self.lst_btn_clear       = window.generator_tab_seed_edit_btn_clear_list
        self.gen_width           = window.generator_tab_seeds_generate_width
        self.gen_height          = window.generator_tab_seeds_generate_height
        self.gen_amount          = window.generator_tab_seeds_generate_amount
        self.gen_btn             = window.generator_tab_seeds_generate_btn
        self.generate_raport_btn = window.generator_tab_btn_raport_generate

    def connect_signals(self):
        self.lst_btn_add.clicked.connect(self.add_maze)
        self.lst_btn_edit.clicked.connect(self.edit_maze)
        self.lst_btn_remove.clicked.connect(self.delete_maze)
        self.lst_btn_clear.clicked.connect(self.clear_list)
        self.gen_btn.clicked.connect(self.generate_seeds)
        self.generate_raport_btn.clicked.connect(self.generate_raport)

    def add_maze(self):
        m = maze.Maze(np.array([int(self.lst_height.text()),
                                int(self.lst_width.text())]),
                                int(self.lst_seed.text()))
        self.state.maze_list.append(m)
        self.update_maze_list_ui()
        self.state.save()

    def edit_maze(self):
        maze_id = self.table.currentRow()
        if maze_id == -1:
            self.status_bar.showMessage('Select row to edit', 2000)
            return
        m = maze.Maze(np.array([int(self.lst_height.text()),
                              int(self.lst_width.text())]),
                              int(self.lst_seed.text()))
        self.state.maze_list[maze_id] = m
        self.update_maze_list_ui()
        self.state.save()

    def delete_maze(self):
        maze_id = self.table.currentRow()
        if maze_id == -1:
            self.status_bar.showMessage('Select row to remove', 2000)
            return
        self.state.maze_list.pop(maze_id)
        self.update_maze_list_ui()
        self.state.save()

    def clear_list(self):
        self.state.maze_list = []
        self.update_maze_list_ui()
        self.state.save()

    def generate_seeds(self):
        for _ in range(int(self.gen_amount.text())):
            m = maze.Maze(np.array([int(self.gen_height.text()),
                                  int(self.gen_width.text())]),
                                  random.randint(0,999999))
            self.state.maze_list.append(m)
        self.update_maze_list_ui()
        self.state.save()

    def generate_raport(self):
        window = QtWidgets.QWidget()
        file_name = QtWidgets.QFileDialog.getSaveFileName(window, 'Save File', '', 'CSV Files (*.csv);;All Files (*)')[0]
        data = [['Lp.', 'Maze height', 'Maze width', 'Maze seed', 'Solver Name', 'Solving time [us]']]
        solvers = [s for s in self.state.solver_list if s.checked]
        row_id = 1
        for m in self.state.maze_list:
            m.generate()
            for s in solvers:
                sol = s.run(m)
                row = [row_id, m.size[0], m.size[1], m.seed, s.name, sol.solving_time_us]
                data.append(row)
                row_id += 1
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def update_maze_list_ui(self):
        self.table.setRowCount(0)
        for m in self.state.maze_list:
            row_id = self.table.rowCount()
            self.table.insertRow(row_id)
            self.table.setItem(row_id,
                               self.col_width,
                               QtWidgets.QTableWidgetItem(str(m.size[1])))
            self.table.setItem(row_id,
                               self.col_height,
                               QtWidgets.QTableWidgetItem(str(m.size[0])))
            self.table.setItem(row_id,
                               self.col_seed,
                               QtWidgets.QTableWidgetItem(str(m.seed)))


class SolversUI:
    def __init__(self, window, state):
        self.state = state
        self.set_constants()
        self.set_references_to_ui_elements(window)
        self.connect_signals()
        self.update_solver_list_ui()

    def set_constants(self):
        self.name_column    = 0
        self.command_column = 1

    def set_references_to_ui_elements(self, window):
        self.status_bar     = window.statusbar
        self.drop_down_list = window.maze_tab_solver_selector
        self.checkable_list = window.generator_tab_solvers_list
        self.table          = window.solvers_tab_list
        self.name           = window.solvers_tab_name
        self.command        = window.solvers_tab_command
        self.btn_add        = window.solvers_tab_btn_add
        self.btn_edit       = window.solvers_tab_btn_edit
        self.btn_remove     = window.solvers_tab_btn_remove

    def connect_signals(self):
        self.checkable_list.itemChanged.connect(self.on_check_update)
        self.btn_add.clicked.connect(self.add_solver)
        self.btn_edit.clicked.connect(self.edit_solver)
        self.btn_remove.clicked.connect(self.remove_solver)

    def add_solver(self):
        s = solver.Solver(self.name.text(), self.command.text(), False)
        self.state.solver_list.append(s)
        self.update_solver_list_ui()
        self.state.save()

    def edit_solver(self):
        solver_id = self.table.currentRow()
        if solver_id == -1:
            self.status_bar.showMessage('Select row to edit', 2000)
            return
        s = solver.Solver(self.name.text(),
                          self.command.text(),
                          self.state.solver_list[solver_id].checked)
        self.state.solver_list[solver_id] = s
        self.update_solver_list_ui()
        self.state.save()

    def remove_solver(self):
        solver_id = self.table.currentRow()
        if solver_id == -1:
            self.status_bar.showMessage('Select row to remove', 2000)
            return
        self.state.solver_list.pop(solver_id)
        self.update_solver_list_ui()
        self.state.save()

    def on_check_update(self, item):
        solver_id = self.checkable_list.row(item)
        self.state.solver_list[solver_id].checked = item.checkState() == QtCore.Qt.Checked
        self.state.save()

    def update_solver_list_ui(self):
        self.drop_down_list.clear()
        self.checkable_list.clear()
        self.table.setRowCount(0)
        for s in self.state.solver_list:
            self.drop_down_list.addItem(s.name)

            item = QtWidgets.QListWidgetItem(s.name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if s.checked:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.checkable_list.addItem(item)

            row_id = self.table.rowCount()
            self.table.insertRow(row_id)
            self.table.setItem(row_id, self.name_column,
                               QtWidgets.QTableWidgetItem(s.name))
            self.table.setItem(row_id, self.command_column,
                               QtWidgets.QTableWidgetItem(s.command))


class MazePainter(QtWidgets.QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.init_canvas(canvas)
        self.m = None
        self.solution = None

    def init_canvas(self, canvas):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self)
        canvas.setLayout(layout)

    def paintEvent(self, event): # Qt name, so pylint: disable=invalid-name
        del event
        # Painting maze
        if self.m is None:
            return
        cell_count = np.array([self.m.size[1], self.m.size[0]])
        cell_wall_length = min(self.width()  / (cell_count[0] + 1),
                               self.height() / (cell_count[1] + 1))
        painter = QtGui.QPainter(self)
        painter.translate((self.width()  - (cell_wall_length * cell_count[0])) // 2,
                          (self.height() - (cell_wall_length * cell_count[1])) // 2)
        painter.scale(cell_wall_length, cell_wall_length)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1)
        pen.setWidth(1 / cell_wall_length)
        painter.setPen(pen)
        # Draw maze frame
        painter.drawLine(0, 0, cell_count[0], 0)
        painter.drawLine(0, 0, 0, cell_count[1])
        painter.drawLine(cell_count[0],
                         cell_count[1],
                         cell_count[0],
                         0)
        painter.drawLine(cell_count[0],
                         cell_count[1],
                         0,
                         cell_count[1])
        # Draw vertical walls
        for x in range(cell_count[0] - 1):
            for y in range(cell_count[1]):
                if self.m.vertical_walls[y][x]:
                    painter.drawLine(x + 1, y, x + 1, y + 1)
        # Draw vertical walls
        for x in range(cell_count[0]):
            for y in range(cell_count[1] - 1):
                if self.m.horizontal_walls[y][x]:
                    painter.drawLine(x, y + 1, x + 1, y + 1)

        painter.scale(0.1, 0.1)

        # Mark start position
        painter.setBrush(QtGui.QColor(0, 255, 0))
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
        painter.setPen(pen)
        x = self.m.start_pos[1]
        y = self.m.start_pos[0]
        painter.drawEllipse(10 * x + 2, 10 * y + 2, 6, 6)
        # Mark finish position
        painter.setBrush(QtGui.QColor(255, 0, 0))
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2)
        painter.setPen(pen)
        x = self.m.finish_pos[1]
        y = self.m.finish_pos[0]
        painter.drawEllipse(10 * x + 2, 10 * y + 2, 6, 6)

        # Painiting solution
        if self.solution is None:
            return

        pen = QtGui.QPen(QtGui.QColor(0, 0, 255), 2)
        painter.setPen(pen)

        prev_cell = None
        for cell in self.solution.path:
            if prev_cell is not None:
                painter.drawLine(10 * prev_cell[1] + 5,
                                 10 * prev_cell[0] + 5,
                                 10 * cell[1] + 5,
                                 10 * cell[0] + 5)
            prev_cell = cell

        # Mark start position
        painter.setBrush(QtGui.QColor(0, 255, 0))
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
        painter.setPen(pen)
        x = self.m.start_pos[1]
        y = self.m.start_pos[0]
        painter.drawEllipse(10 * x + 2, 10 * y + 2, 6, 6)
        # Mark finish position
        painter.setBrush(QtGui.QColor(255, 0, 0))
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2)
        painter.setPen(pen)
        x = self.m.finish_pos[1]
        y = self.m.finish_pos[0]
        painter.drawEllipse(10 * x + 2, 10 * y + 2, 6, 6)

    def paint_maze(self, m):
        self.m = m
        self.solution = None
        self.update()

    def paint_solution(self, solution):
        self.solution = solution
        self.update()
