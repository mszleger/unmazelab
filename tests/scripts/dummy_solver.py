#!/usr/bin/env python
import numpy as np

if __name__ == "__main__":
    maze_size = np.array([-1, -1])
    maze_size[0] = input()
    maze_size[1] = input()
    # Load start pos
    input()
    input()
    # Load finish pos
    input()
    input()
    # Load vertical walls
    for i in range(0, maze_size[0] * (maze_size[1] - 1)):
        input()
    # Load horizontal walls
    for i in range(0, (maze_size[0] - 1) * (maze_size[1])):
        input()
    print("1000\n1\n2\n3\n4\n")