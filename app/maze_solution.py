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
        values = frame.strip().split('\n')
        self.solving_time_us = int(values.pop(0))
        path = []
        while values:
            pos = np.array([int(values.pop(0)),
                            int(values.pop(0))])
            path.append(pos)
        self.path = np.array(path)