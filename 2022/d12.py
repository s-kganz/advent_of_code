import numpy as np
from queue import PriorityQueue


grid = open("2022/d12_input.txt").read()
nrow = grid.count("\n")
ncol = grid.index("\n")

grid = grid.replace("\n", "")

# Find start and end positions
start_index = grid.index("S")
end_index = grid.index("E")
startx = start_index % ncol
starty = start_index // ncol
endx = end_index % ncol
endy = end_index // ncol

grid = np.array(list(grid.replace("\n", ""))).reshape((nrow, ncol))

# Make sure start and end were found correctly
# print(grid[endy, endx])
# print(grid[starty, startx])

# Convert the array to numbers


def char_to_int(c):
    if c == "E":
        return 25
    elif c == "S":
        return 0
    else:
        return ord(c) - 97

# Go easy on me I've never implemented Djikstra's before


def get_if_inbounds(grid, x, y):
    # Return elevation at grid[y, x] if the coords are
    # inbounds, otherwise return -1.
    if y >= 0 and y < grid.shape[0] and x >= 0 and x < grid.shape[1]:
        return grid[y, x]
    else:
        return -1


def reachable(grid, x1, y1, x2, y2):
    # Return if x2, y2 is inbounds and reachable from x1, y1
    if get_if_inbounds(grid, x2, y2) == -1:
        return False
    else:
        # Elevation can be at most grid[y1, x1] + 1
        return get_if_inbounds(grid, x2, y2) <= get_if_inbounds(grid, x1, y1)+1

grid = np.vectorize(char_to_int)(grid)

def shortest_path(grid, startx, starty, endx, endy):
    steps = [
        (1,  0),
        (-1,  0),
        (0,  1),
        (0, -1)
    ]

    # Determine what "infinity" is in this case
    max_path_length = grid.shape[0] * grid.shape[1] + 1

    # Initialize the distance matrix
    dist = np.zeros(grid.shape[0]*grid.shape[1]).reshape(grid.shape) + max_path_length
    dist[starty, startx] = 0

    # Initialize the visited matrid
    visited = np.zeros(nrow*ncol).reshape(grid.shape)

    while not np.all(visited == 1):
        yarr, xarr = np.where(np.logical_and(visited == 0, dist == np.min(dist[visited == 0])))
        if xarr.shape[0] == 0 and yarr.shape[0] == 0:
            break
        thisx, thisy = xarr[0], yarr[0]
        visited[thisy, thisx] = 1

        if (thisx == endx and thisy == endy):
            return dist[thisy, thisx]

        for (dx, dy) in filter(
            lambda step: reachable(grid, thisx, thisy, thisx+step[0], thisy+step[1]),
            steps
        ):
            altdist = dist[thisy, thisx] + 1
            if altdist < dist[thisy+dy, thisx+dx]:
                dist[thisy+dy, thisx+dx] = altdist

# Part 1
print(shortest_path(grid, startx, starty, endx, endy))

# Part 2
print("Testing {} starting positions".format(np.sum(grid == 0)))
print(min(shortest_path(grid, sx, sy, endx, endy) for (sy, sx) in zip(*np.where(grid == 0))))
