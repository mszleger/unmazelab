from app.maze import Maze
from app.maze_solution import MazeSolution
from app.utilities import call_command

class Solver:
    def __init__(self, name, command):
        self.__name = name
        self.__command = command

    def get_name(self):
        return self.__name

    def get_command(self):
        return self.__command

    def run(self, maze):
        solution = MazeSolution(self.__name)
        output = call_command(self.__command, maze.get_frame_for_solver())
        solution.load_solution_from_solver(output)
        return solution