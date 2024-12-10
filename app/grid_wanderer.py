import numpy as np

class GridWanderer:
    def __init__(self, size):
        self.size = size

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
        self._visited_tiles = np.zeros((size[0], size[1]), dtype=bool)

    @property
    def current_pos(self):
        return self._current_pos

    @current_pos.setter
    def current_pos(self, current_pos):
        if type(current_pos) != np.ndarray:
            raise ValueError("Current position must be numpy.ndarray")
        if current_pos.size != 2 or current_pos.shape[0] != 2:
            raise ValueError("Current position must be one dimensional array with two values")
        if (current_pos < 0).any() or current_pos[0] >= self.size[0] or current_pos[1] >= self.size[1]:
            raise ValueError("Current position is outside of the grid")
        self._current_pos = current_pos
        self._visited_tiles[current_pos[0]][current_pos[1]] = True

    def get_all_neighbours(self):
        vects_to_neighbours = np.array([[-1,  0],
                                        [ 1,  0],
                                        [ 0, -1],
                                        [ 0,  1]])
        neighbours = self.current_pos + vects_to_neighbours
        neighbours = neighbours[(neighbours[:, 0] >= 0)
                              & (neighbours[:, 1] >= 0)
                              & (neighbours[:, 0] <  self.size[0])
                              & (neighbours[:, 1] <  self.size[1])]
        return np.array(neighbours)

    def get_unvisited_neighbours(self):
        unvisited_neighbours = []
        for pos in self.get_all_neighbours():
            if not self._visited_tiles[pos[0]][pos[1]]:
                unvisited_neighbours.append(pos)
        return np.array(unvisited_neighbours)