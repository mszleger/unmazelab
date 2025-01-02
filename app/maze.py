from multipledispatch import dispatch
import numpy as np
import random
import xml.etree.ElementTree as ET

from app import utilities


class Maze:
    @dispatch(int, int, int)
    def __init__(self, height, width, seed):
        self.size = np.array([height, width])
        self.seed = seed

    @dispatch(np.ndarray, int)
    def __init__(self, size, seed):
        self.size = size
        self.seed = seed

    @dispatch(ET.Element)
    def __init__(self, xml_config_tree_root):
        self.load(xml_config_tree_root)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if type(size) != np.ndarray:
            raise ValueError("Size must be numpy.ndarray")
        if size.size != 2 or size.shape[0] != 2:
            raise ValueError("Size must be one dimensional array with two values")
        if (size < 2).any():
            raise ValueError("Both values of size must be equal or greater than 2")
        self._size = size
        self._start_pos = None
        self._finish_pos = None
        self.vertical_walls = None
        self.horizontal_walls = None

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        if type(seed) != int:
            raise ValueError("Seed must be integer")
        self._seed = seed

    @property
    def start_pos(self):
        return self._start_pos

    @start_pos.setter
    def start_pos(self, start_pos):
        if type(start_pos) != np.ndarray:
            raise ValueError("Start position must be numpy.ndarray")
        if start_pos.size != 2 or start_pos.shape[0] != 2:
            raise ValueError("Start position must be one dimensional array with two values")
        if (start_pos < 0).any() or start_pos[0] >= self.size[0] or start_pos[1] >= self.size[1]:
            raise ValueError("Start position is outside of the maze")
        self._start_pos = start_pos

    @property
    def finish_pos(self):
        return self._finish_pos

    @finish_pos.setter
    def finish_pos(self, finish_pos):
        if type(finish_pos) != np.ndarray:
            raise ValueError("Finish position must be numpy.ndarray")
        if finish_pos.size != 2 or finish_pos.shape[0] != 2:
            raise ValueError("Finish position must be one dimensional array with two values")
        if (finish_pos < 0).any() or finish_pos[0] >= self.size[0] or finish_pos[1] >= self.size[1]:
            raise ValueError("Finish position is outside of the maze")
        self._finish_pos = finish_pos

    def load(self, xml_config_tree_root):
        self.size = np.array([int(xml_config_tree_root.find("height").text),
                              int(xml_config_tree_root.find("width").text)])
        self.seed = int(xml_config_tree_root.find("seed").text)

    def save(self, xml_config_tree_root):
        ET.SubElement(xml_config_tree_root, "height").text = str(self.size[0])
        ET.SubElement(xml_config_tree_root, "width").text = str(self.size[1])
        ET.SubElement(xml_config_tree_root, "seed").text = str(self.seed)

    def generate(self):
        random.seed(self.seed)
        self.generate_walls()
        self.generate_start_pos()
        self.generate_finish_pos()

    def generate_start_pos(self): # Just set default start position to (0, 0)
        mw = MazeWanderer(self)
        g = mw.get_grid_with_distanses_from_pos(np.array([self.size[0] - 1, self.size[1] - 1]))
        pos = g.argmax()
        self.start_pos = np.array([pos // self.size[1], pos % self.size[1]])

    def generate_finish_pos(self): # Just set default finish position to (height - 1, width - 1)
        mw = MazeWanderer(self)
        g = mw.get_grid_with_distanses_from_pos(self.start_pos)
        pos = g.argmax()
        self.finish_pos = np.array([pos // self.size[1], pos % self.size[1]])

    def generate_walls(self):
        gw = GridWanderer(self.size)
        self.set_walls_everywhere()
        for row in range(0, self.size[0]):
            for col in range(0, self.size[1]):
                while(True):
                    gw.current_pos = np.array([row, col])
                    unvisited_neighbours = gw.get_unvisited_neighbours()
                    if unvisited_neighbours.size == 0:
                        break
                    while True:
                        new_pos = random.choice(unvisited_neighbours)
                        self.remove_wall_between_neighbours(gw.current_pos, new_pos)
                        gw.current_pos = new_pos
                        unvisited_neighbours = gw.get_unvisited_neighbours()
                        if unvisited_neighbours.size == 0:
                            break

    def set_walls_everywhere(self):
        self.vertical_walls   = np.ones((self.size[0],     self.size[1] - 1), dtype=bool)
        self.horizontal_walls = np.ones((self.size[0] - 1, self.size[1]    ), dtype=bool)

    def remove_wall_between_neighbours(self, pos_1, pos_2):
        vect = pos_2 - pos_1
        if vect[0] == -1 and vect[1] == 0:
            self.horizontal_walls[pos_1[0] - 1][pos_1[1]] = False
        elif vect[0] == 1 and vect[1] == 0:
            self.horizontal_walls[pos_1[0]][pos_1[1]] = False
        elif vect[0] == 0 and vect[1] == -1:
            self.vertical_walls[pos_1[0]][pos_1[1] - 1] = False
        elif vect[0] == 0 and vect[1] == 1:
            self.vertical_walls[pos_1[0]][pos_1[1]] = False
        else:
            raise ValueError('Positions are not neighbours')

    def get_frame_for_solver(self): # move to Solver class
        frame  = f'{self.size[0]}\n{self.size[1]}\n'
        frame += f'{self.start_pos[0]}\n{self.start_pos[1]}\n'
        frame += f'{self.finish_pos[0]}\n{self.finish_pos[1]}\n'
        for value in np.nditer(self.vertical_walls):
            frame += f'{int(value)}\n'
        for value in np.nditer(self.horizontal_walls):
            frame += f'{int(value)}\n'
        return frame


class GridWanderer:
    """
    A class to represent a wandering on grid.

    The grid is two dimensional array with given height and width, containing information about visited and unvisited cells.

    Attributes:
        size (np.ndarray): Array with height and width of grid.
        grid (np.ndarray): Array with vertical and horizontal position.
        _visited_tiles (np.ndarray): Array representing grid containig values of visited and unvisited positions.

    Methods:
        get_all_neighbours(): Return array of positions next to current position.
        get_unvisited_neighbours(): Return array of unvisited positions next to current position.
    """
    def __init__(self, size: np.ndarray):
        """
        Initialize size of grid.

        :param size: Array with height and width of grid.
        :type size: np.ndarray
        """
        self.size = size

    @property
    def size(self) -> np.ndarray:
        """
        Return size of grid.

        :return: Array with height and width of grid.
        :rtype: np.ndarray
        """
        return self._size

    @size.setter
    def size(self, size: np.ndarray):
        """
        Set size of grid.

        Validate new size of grid, set size, reset value of current position to None and create grid with given size full of unvisited positions.

        :param size: Array with height and width of grid.
        :type size: np.ndarray

        :raises ValueError: If size isn't one dimensional np.ndarray with two values.
        """
        if type(size) != np.ndarray:
            raise ValueError("Size must be numpy.ndarray")
        if size.size != 2 or size.shape[0] != 2:
            raise ValueError("Size must be one dimensional array with two values")
        if (size < 2).any():
            raise ValueError("Both values of size must be equal or greater than 2")
        self._size = size
        self._current_pos = None
        self._visited_tiles = np.zeros((size[0], size[1]), dtype=bool)

    @property
    def current_pos(self) -> np.ndarray:
        """
        Return current position in grid.

        :return: Array with vertical and horizontal position.
        :rtype: np.ndarray
        """
        return self._current_pos

    @current_pos.setter
    def current_pos(self, current_pos: np.ndarray):
        """
        Set current position in grid.

        Validate new position, set it and mark new cell as visited.

        :param size: Array with vertical and horizontal position.
        :type size: np.ndarray

        :raises ValueError: If size isn't one dimensional np.ndarray with two values or position is outside grid.
        """
        if type(current_pos) != np.ndarray:
            raise ValueError("Current position must be numpy.ndarray")
        if current_pos.size != 2 or current_pos.shape[0] != 2:
            raise ValueError("Current position must be one dimensional array with two values")
        if (current_pos < 0).any() or current_pos[0] >= self.size[0] or current_pos[1] >= self.size[1]:
            raise ValueError("Current position is outside of the grid")
        self._current_pos = current_pos
        self._visited_tiles[current_pos[0]][current_pos[1]] = True

    def get_all_neighbours(self) -> np.ndarray:
        """
        Return array of positions next to current position.

        Return array of valid positions next to current position (UP, DOWN, LEFT, RIGHT).

        :return: Two dimnsional array with positions of neighbours as arrays with vertical and horizontal position.
        :rtype: np.ndarray
        """
        vects_to_neighbours = np.array([[-1,  0],
                                        [ 1,  0],
                                        [ 0, -1],
                                        [ 0,  1]])
        neighbours = self.current_pos + vects_to_neighbours
        neighbours = neighbours[(neighbours[:, 0] >= 0)
                              & (neighbours[:, 1] >= 0)
                              & (neighbours[:, 0] <  self.size[0])
                              & (neighbours[:, 1] <  self.size[1])]
        return neighbours

    def get_unvisited_neighbours(self) -> np.ndarray:
        """
        Return array of unvisited positions next to current position.

        Return array of valid and unvisited positions next to current position (UP, DOWN, LEFT, RIGHT).

        :return: Two dimnsional array with positions of neighbours as arrays with vertical and horizontal position.
        :rtype: np.ndarray
        """
        unvisited_neighbours = []
        for pos in self.get_all_neighbours():
            if not self._visited_tiles[pos[0]][pos[1]]:
                unvisited_neighbours.append(pos)
        return np.array(unvisited_neighbours)


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


class MazeWanderer:
    def __init__(self, maze):
        self.maze = maze
        self.grid = np.full([self.maze.size[0], self.maze.size[1]], -1)

    def get_grid_with_distanses_from_pos(self, pos):
        self.grid = np.full([self.maze.size[0], self.maze.size[1]], -1)
        current_positions = [pos]
        current_step = 0
        while len(current_positions) != 0:
            new_positions = []
            for pos in current_positions:
                self.grid[pos[0]][pos[1]] = current_step
                new_positions.extend(self.get_nonvisited_accessible_neighbours(pos))
            current_positions = new_positions
            current_step += 1
        return self.grid

    def get_nonvisited_accessible_neighbours(self, pos):
        neighbours = self.get_all_accessible_neighbours(pos)
        non_visited = []
        for n in neighbours:
            if self.grid[n[0]][n[1]] == -1:
                non_visited.append(n)
        return np.array(non_visited)

    def get_all_accessible_neighbours(self, pos):
        neighbours = []
        # Up
        if pos[0] > 0:
            if self.maze.horizontal_walls[pos[0] - 1][pos[1]] == False:
                neighbours.append(np.array([pos[0] - 1, pos[1]]))
        # Down
        if pos[0] < self.maze.size[0] - 1:
            if self.maze.horizontal_walls[pos[0]][pos[1]] == False:
                neighbours.append(np.array([pos[0] + 1, pos[1]]))
        # Left
        if pos[1] > 0:
            if self.maze.vertical_walls[pos[0]][pos[1] - 1] == False:
                neighbours.append(np.array([pos[0], pos[1] - 1]))
        # Right
        if pos[1] < self.maze.size[1] - 1:
            if self.maze.vertical_walls[pos[0]][pos[1]] == False:
                neighbours.append(np.array([pos[0], pos[1] + 1]))
        return np.array(neighbours)


class Solver:
    @dispatch(str, str, bool)
    def __init__(self, name, command, checked):
        self.name = name
        self.command = command
        self.checked = checked

    @dispatch(ET.Element)
    def __init__(self, xml_config_tree_root):
        self.load(xml_config_tree_root)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) != str:
            raise ValueError("Name must be string")
        if len(name) == 0:
            raise ValueError("Name can't be empty string")
        self._name = name

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        if type(command) != str:
            raise ValueError("Command must be string")
        if len(command) == 0:
            raise ValueError("Command can't be empty string")
        self._command = command

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, checked):
        if type(checked) != bool:
            raise ValueError("Checked must be boolean")
        self._checked = checked

    def load(self, xml_config_tree_root):
        self.name = xml_config_tree_root.find("name").text
        self.command = xml_config_tree_root.find("command").text
        self.checked = (xml_config_tree_root.find("checked").text == "True")

    def save(self, xml_config_tree_root):
        ET.SubElement(xml_config_tree_root, "name").text = self.name
        ET.SubElement(xml_config_tree_root, "command").text = self.command
        if self.checked:
            ET.SubElement(xml_config_tree_root, "checked").text = "True"
        else:
            ET.SubElement(xml_config_tree_root, "checked").text = "False"

    def run(self, maze):
        output_frame = utilities.call_command(self.command, maze.get_frame_for_solver())
        solution = MazeSolution(output_frame)
        return solution

class Vector2D:
    """
    A class to represent a 2D vector.

    Attributes:
        x (int): X position of vector.
        y (int): Y position of vector.
    """
    def __init__(self, x, y):
        """
        Initialize values of vector.

        :param x: X position of vector.
        :type x: int
        :param y: Y position of vector.
        :type y: int
        """
        self.x = x
        self.y = y

    @property
    def x(self):
        """
        Getter of x value of vector.

        :return: X position of vector.
        :rtype: int
        """
        return self._x

    @x.setter
    def x(self, x):
        """
        Setter of x value of vector.

        :param x: X position of vector.
        :type x: int

        :raises ValueError: If x isn't of type int.
        """
        if type(x) != int:
            raise ValueError("X has to be value of type int")
        self._x = x

    @property
    def y(self):
        """
        Getter of y value of vector.

        :return: Y position of vector.
        :rtype: int
        """
        return self._y

    @y.setter
    def y(self, y):
        """
        Setter of y value of vector.

        :param y: Y position of vector.
        :type y: int

        :raises ValueError: If y isn't of type int.
        """
        if type(y) != int:
            raise ValueError("Y has to be value of type int")
        self._y = y

    def __str__(self):
        """
        Dunder returning string representation of vector.

        :return: String representation of vector.
        :rtype: str
        """
        return f'({self.x}, {self.y})'

    def __repr__(self):
        """
        Dunder returning string representation of vector.

        :return: String representation of vector.
        :rtype: str
        """
        return f'({self.x}, {self.y})'