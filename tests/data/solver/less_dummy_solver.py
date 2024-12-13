import numpy as np
import time

class Maze:
    def load(self):
        self.size = np.array([int(input()), int(input())])
        self.start_pos = np.array([int(input()), int(input())])
        self.finish_pos = np.array([int(input()), int(input())])
        self.vertical_walls   = np.zeros((self.size[0],     self.size[1] - 1), dtype=bool)
        self.horizontal_walls = np.zeros((self.size[0] - 1, self.size[1]    ), dtype=bool)
        for x in range(self.size[0]):
            for y in range(self.size[1] - 1):
                self.vertical_walls[x][y] = (input() == '1')
        for x in range(self.size[0] - 1):
            for y in range(self.size[1]):
                self.horizontal_walls[x][y] = (input() == '1')

    def fill_with_water(self):
        self.grid = np.full([self.size[0], self.size[1]], -1)
        current_positions = []
        current_positions.append(self.start_pos.copy())
        current_step = 0
        while len(current_positions) != 0:
            new_positions = []
            for pos in current_positions:
                self.grid[pos[0]][pos[1]] = current_step
                new_positions.extend(self.get_nonvisited_neighbours(pos))
            current_positions = new_positions
            current_step += 1

    def get_nonvisited_neighbours(self, pos):
        neighbours = self.get_all_neighbours(pos)
        non_visited = []
        for n in neighbours:
            if self.grid[n[0]][n[1]] == -1:
                non_visited.append(n)
        return non_visited

    def get_backtracked_path(self):
        reversed_path = []
        pos = self.finish_pos
        reversed_path.append(pos)
        while not (pos == self.start_pos).all():
            neighbours = self.get_all_neighbours(pos)
            current_step = self.grid[pos[0]][pos[1]]
            for n in neighbours:
                if self.grid[n[0]][n[1]] == (current_step - 1):
                    pos = n
                    reversed_path.append(pos)
                    break
        reversed_path.reverse()
        return reversed_path

    def get_all_neighbours(self, pos):
        neighbours = []
        # Up
        if pos[0] > 0:
            if self.horizontal_walls[pos[0] - 1][pos[1]] == False:
                neighbours.append(np.array([pos[0] - 1, pos[1]]))
        # Down
        if pos[0] < self.size[0] - 1:
            if self.horizontal_walls[pos[0]][pos[1]] == False:
                neighbours.append(np.array([pos[0] + 1, pos[1]]))
        # Left
        if pos[1] > 0:
            if self.vertical_walls[pos[0]][pos[1] - 1] == False:
                neighbours.append(np.array([pos[0], pos[1] - 1]))
        # Right
        if pos[1] < self.size[1] - 1:
            if self.vertical_walls[pos[0]][pos[1]] == False:
                neighbours.append(np.array([pos[0], pos[1] + 1]))
        return np.array(neighbours)

if __name__ == "__main__":
    m = Maze()
    m.load()

    start_time = time.time()
    m.fill_with_water()
    path = m.get_backtracked_path()
    end_time = time.time()

    execution_time_s = end_time - start_time
    execution_time_us = int(execution_time_s * 1_000_000)
    print(execution_time_us)
    for pos in path:
        print(pos[0])
        print(pos[1])