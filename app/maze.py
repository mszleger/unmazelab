from app.grid_wanderer import GridWanderer
import numpy as np
import random

class Maze:
    def __init__(self, size, seed):
        self.__size = size.copy()
        self.__generate(seed)

    def __generate(self, seed):
        random.seed(seed)
        self.__generate_start_pos()
        self.__generate_finish_pos()
        self.__generate_walls()

    def __generate_start_pos(self):
        self.__start_pos = np.array([random.randint(0, self.__size[0] - 1), random.randint(0, self.__size[1] - 1)])

    def __generate_finish_pos(self):
        while True:
            self.__finish_pos = np.array([random.randint(0, self.__size[0] - 1), random.randint(0, self.__size[1] - 1)])
            if (self.__start_pos != self.__finish_pos).any():
                break

    def __generate_walls(self):
        gw = GridWanderer(self.__size)
        self.__set_walls_everywhere()
        for row in range(0, self.__size[0]):
            for col in range(0, self.__size[1]):
                pos = np.array([row, col])
                gw.set_current_pos(pos)
                while True:
                    unvisited_neighbours = gw.get_unvisited_neighbours()
                    if unvisited_neighbours.size == 0:
                        break
                    gw.set_current_pos(random.choice(unvisited_neighbours))
                    new_pos = gw.get_current_pos()
                    self.__remove_wall_between_neighbours(pos, new_pos)
                    pos = new_pos

    def __set_walls_everywhere(self):
        self.__vertical_walls   = np.ones((self.__size[0],     self.__size[1] - 1), dtype=bool)
        self.__horizontal_walls = np.ones((self.__size[0] - 1, self.__size[1]    ), dtype=bool)

    def __remove_wall_between_neighbours(self, pos_1, pos_2):
        vect = pos_2 - pos_1
        if vect[0] == -1 and vect[1] == 0:
            self.__horizontal_walls[pos_1[0] - 1][pos_1[1]] = False
        elif vect[0] == 1 and vect[1] == 0:
            self.__horizontal_walls[pos_1[0]][pos_1[1]] = False
        elif vect[0] == 0 and vect[1] == -1:
            self.__vertical_walls[pos_1[0]][pos_1[1] - 1] = False
        elif vect[0] == 0 and vect[1] == 1:
            self.__vertical_walls[pos_1[0]][pos_1[1]] = False

    def get_size(self):
        return self.__size.copy()

    def get_start_pos(self):
        return self.__start_pos.copy()

    def get_finish_pos(self):
        return self.__finish_pos.copy()

    def get_vertical_walls(self):
        return self.__vertical_walls.copy()

    def get_horizontal_walls(self):
        return self.__horizontal_walls.copy()

    def get_frame_for_solver(self):
        frame  = f'{self.__size[0]}\n{self.__size[1]}\n'
        frame += f'{self.__start_pos[0]}\n{self.__start_pos[1]}\n'
        frame += f'{self.__finish_pos[0]}\n{self.__finish_pos[1]}\n'
        for value in np.nditer(self.__vertical_walls):
            frame += f'{int(value)}\n'
        for value in np.nditer(self.__horizontal_walls):
            frame += f'{int(value)}\n'
        return frame