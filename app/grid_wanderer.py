import numpy as np

class GridWanderer:
    def __init__(self, size):
        self.__size = size
        self.__visited_tiles = np.zeros((size[0], size[1]), dtype=bool)

    def set_current_pos(self, pos):
        self.__current_pos = pos
        self.__visited_tiles[pos[0]][pos[1]] = True

    def get_current_pos(self):
        return self.__current_pos

    def get_all_neighbours(self):
        vects_to_neighbours = np.array([[-1,  0],
                                        [ 1,  0],
                                        [ 0, -1],
                                        [ 0,  1]])
        neighbours = self.__current_pos + vects_to_neighbours
        neighbours = neighbours[(neighbours[:, 0] >= 0)
                              & (neighbours[:, 1] >= 0)
                              & (neighbours[:, 0] <  self.__size[0])
                              & (neighbours[:, 1] <  self.__size[1])]
        return np.array(neighbours)

    def get_unvisited_neighbours(self):
        unvisited_neighbours = []
        for pos in self.get_all_neighbours():
            if not self.__visited_tiles[pos[0]][pos[1]]:
                unvisited_neighbours.append(pos)
        return np.array(unvisited_neighbours)