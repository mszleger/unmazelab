import numpy as np
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout

class MazePainter(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.init_canvas(canvas)
        self.maze = None
        self.solution = None

    def init_canvas(self, canvas):
        layout = QVBoxLayout()
        layout.addWidget(self)
        canvas.setLayout(layout)

    def paintEvent(self, event):
        if type(self.maze) == type(None):
            return
        cell_count = np.array([self.maze.size[1], self.maze.size[0]])
        cell_wall_length = min(self.width() / (cell_count[0] + 1), self.height() / (cell_count[1] + 1))
        painter = QPainter(self)
        painter.translate((self.width()  - (cell_wall_length * cell_count[0])) // 2,
                          (self.height() - (cell_wall_length * cell_count[1])) // 2)
        painter.scale(cell_wall_length, cell_wall_length)
        pen = QPen(QColor(0, 0, 0), 1)
        pen.setWidth(1 / cell_wall_length)
        painter.setPen(pen)
        # Draw maze frame
        painter.drawLine(0,             0,             cell_count[0], 0)
        painter.drawLine(0,             0,             0,             cell_count[1])
        painter.drawLine(cell_count[0], cell_count[1], cell_count[0], 0)
        painter.drawLine(cell_count[0], cell_count[1], 0,             cell_count[1])
        # Draw vertical walls
        for x in range(cell_count[0] - 1):
            for y in range(cell_count[1]):
                if(self.maze.vertical_walls[y][x]):
                    painter.drawLine(x + 1, y, x + 1, y + 1)
        # Draw vertical walls
        for x in range(cell_count[0]):
            for y in range(cell_count[1] - 1):
                if(self.maze.horizontal_walls[y][x]):
                    painter.drawLine(x, y + 1, x + 1, y + 1)

    def paint_maze(self, maze):
        self.maze = maze
        self.update()

    def paint_solution(self, solution):
        self.solution = solution
        self.update()