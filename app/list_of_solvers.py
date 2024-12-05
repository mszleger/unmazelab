from app.solver import Solver

class ListOfSovers:
    def __init__(self):
        self.__solvers = []

    def add(self, solver):
        self.__solvers.append(solver)

    def get(self, solver_id):
        return self.__solvers[solver_id]

    def edit(self, solver_id, solver):
        self.__solvers[solver_id] = solver

    def remove(self, solver_id):
        self.__solvers.pop(solver_id)

    def switch_places(self, solver_1_id, solver_2_id):
        self.__solvers[solver_1_id], self.__solvers[solver_2_id] = self.__solvers[solver_2_id], self.__solvers[solver_1_id]

    def run(self, solvers_id_list, maze):
        output = []
        for id in solvers_id_list:
            output.append(self.__solvers[id].run(maze))
        return output