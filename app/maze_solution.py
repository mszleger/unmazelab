import numpy as np

class MazeSolution:
    def __init__(self, solver_name):
        self.__solver_name = solver_name
        self.__solving_time = None
        self.__path = np.array([])

    def load_solution_from_solver(self, frame):
        values = frame.strip().split('\n')
        self.__solving_time = int(values.pop(0))
        path = []
        while values:
            pos = np.array([-1, -1])
            pos[0] = int(values.pop(0))
            pos[1] = int(values.pop(0))
            path.append(pos)
        self.__path = np.array(path)

    def get_solver_name(self):
        return self.__solver_name

    def get_solving_time(self):
        return self.__solving_time

    def get_path(self):
        return self.__path.copy()