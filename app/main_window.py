import sys
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from app.app_state import AppState
from app.maze_visualizer_tab import MazeVisualizerTab
from app.raport_generator_tab import RaportGeneratorTab
from app.solvers_ui import SolversUI

class MainWindow:
    def __init__(self, app_state):
        self.app_state = app_state
        self.app = QApplication(sys.argv)
        self.load_ui("app/ui/main_window.ui")
        self.connect_signals()
        self.window.show()
        sys.exit(self.app.exec())

    def load_ui(self, file_name):
        ui_file = QFile(file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        if not self.window:
            print(loader.errorString())
            sys.exit(-1)

    def connect_signals(self):
        self.maze_visualizer_tab = MazeVisualizerTab(self.window, self.app_state)
        self.raport_generator_tab = RaportGeneratorTab(self.window, self.app_state)
        self.solvers_ui = SolversUI(self.window, self.app_state)