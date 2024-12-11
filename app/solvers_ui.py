from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

from app.solver import Solver

class SolversUI:
    def __init__(self, window, app_state):
        self.app_state = app_state
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
        solver = Solver(self.name.text(), self.command.text(), False)
        self.app_state.solver_list.append(solver)
        self.update_solver_list_ui()
        self.app_state.save()

    def edit_solver(self):
        solver_id = self.table.currentRow()
        if solver_id == -1:
            self.status_bar.showMessage("Select row to edit", 2000)
            return
        solver = Solver(self.name.text(), self.command.text(), self.app_state.solver_list[solver_id].checked)
        self.app_state.solver_list[solver_id] = solver
        self.update_solver_list_ui()
        self.app_state.save()

    def remove_solver(self):
        solver_id = self.table.currentRow()
        if solver_id == -1:
            self.status_bar.showMessage("Select row to remove", 2000)
            return
        self.app_state.solver_list.pop(solver_id)
        self.update_solver_list_ui()
        self.app_state.save()

    def on_check_update(self, item):
        solver_id = self.checkable_list.row(item)
        self.app_state.solver_list[solver_id].checked = (item.checkState() == Qt.Checked)
        self.app_state.save()

    def update_solver_list_ui(self):
        self.drop_down_list.clear()
        self.checkable_list.clear()
        self.table.setRowCount(0)
        for solver in self.app_state.solver_list:
            self.drop_down_list.addItem(solver.name)

            item = QListWidgetItem(solver.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if solver.checked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.checkable_list.addItem(item)

            row_id = self.table.rowCount()
            self.table.insertRow(row_id)
            self.table.setItem(row_id, self.name_column,    QTableWidgetItem(solver.name))
            self.table.setItem(row_id, self.command_column, QTableWidgetItem(solver.command))