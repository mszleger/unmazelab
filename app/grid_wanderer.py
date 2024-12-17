import numpy as np

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