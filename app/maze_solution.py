from multipledispatch import dispatch
import numpy as np

class MazeSolution:
    @dispatch(int, np.ndarray)
    def __init__(self, solving_time_us, path):
        self.solving_time_us = solving_time_us
        self.path = path

    @dispatch(str)
    def __init__(self, solver_output_frame):
        self.load_solver_output_frame(solver_output_frame)

    @property
    def solving_time_us(self):
        return self._solving_time_us

    @solving_time_us.setter
    def solving_time_us(self, solving_time_us):
        if type(solving_time_us) != int:
            raise ValueError("Solving time must be integer")
        self._solving_time_us = solving_time_us

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if type(path) != np.ndarray:
            raise ValueError("Path must be numpy.ndarray")
        if path.shape[1] != 2:
            raise ValueError("Path must have two columns")
        if path.shape[0] < 2:
            raise ValueError("Path must have at least two rows")
        self._path = path

    def load_solver_output_frame(self, frame):
        values = frame.split()
        if len(values) % 2 != 1:
            raise ValueError('Incorrect length of output frame from solver')
        values = [int(value) if value.isnumeric() else None for value in values]
        if None in values:
            raise ValueError('Output frame from solver contain non numeric characters')
        self.solving_time_us = values.pop(0)
        path = []
        while values:
            pos = np.array([values.pop(0),
                            values.pop(0)])
            path.append(pos)
        self.path = np.array(path)