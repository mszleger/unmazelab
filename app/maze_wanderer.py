import numpy as np

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