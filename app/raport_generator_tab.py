import csv
import numpy as np
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QWidget
import random

from app.maze import Maze

class RaportGeneratorTab:
    def __init__(self, window, app_state):
        self.app_state = app_state
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
        self.app_state.maze_list.append(Maze(np.array([int(self.lst_height.text()),
                                                       int(self.lst_width.text())]),
                                                       int(self.lst_seed.text())))
        self.update_maze_list_ui()
        self.app_state.save()

    def edit_maze(self):
        maze_id = self.table.currentRow()
        if maze_id == -1:
            self.status_bar.showMessage("Select row to edit", 2000)
            return
        maze = Maze(np.array([int(self.lst_height.text()),
                              int(self.lst_width.text())]),
                              int(self.lst_seed.text()))
        self.app_state.maze_list[maze_id] = maze
        self.update_maze_list_ui()
        self.app_state.save()

    def delete_maze(self):
        maze_id = self.table.currentRow()
        if maze_id == -1:
            self.status_bar.showMessage("Select row to remove", 2000)
            return
        self.app_state.maze_list.pop(maze_id)
        self.update_maze_list_ui()
        self.app_state.save()

    def clear_list(self):
        self.app_state.maze_list = []
        self.update_maze_list_ui()
        self.app_state.save()

    def generate_seeds(self):
        for i in range(int(self.gen_amount.text())):
            maze = Maze(np.array([int(self.gen_height.text()),
                                  int(self.gen_width.text())]),
                                  random.randint(0,999999))
            self.app_state.maze_list.append(maze)
        self.update_maze_list_ui()
        self.app_state.save()

    def generate_raport(self):
        window = QWidget()
        file_name = QFileDialog.getSaveFileName(window, "Save File", "", "CSV Files (*.csv);;All Files (*)")[0]
        data = [['Lp.', 'Maze height', 'Maze width', 'Maze seed', 'Solver Name', 'Solving time [us]']]
        solvers = [s for s in self.app_state.solver_list if s.checked]
        row_id = 1
        for m in self.app_state.maze_list:
            m.generate()
            for s in solvers:
                sol = s.run(m)
                row = [row_id, m.size[0], m.size[1], m.seed, s.name, sol.solving_time_us]
                data.append(row)
                row_id += 1
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def update_maze_list_ui(self):
        self.table.setRowCount(0)
        for maze in self.app_state.maze_list:
            row_id = self.table.rowCount()
            self.table.insertRow(row_id)
            self.table.setItem(row_id, self.col_width,  QTableWidgetItem(str(maze.size[1])))
            self.table.setItem(row_id, self.col_height, QTableWidgetItem(str(maze.size[0])))
            self.table.setItem(row_id, self.col_seed,   QTableWidgetItem(str(maze.seed)))