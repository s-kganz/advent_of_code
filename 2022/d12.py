import numpy as np

grid = open("2022/d12_input.txt").read()
nrow = grid.count("\n")
ncol = grid.index("\n")

grid = grid.replace("\n", "")

# Find start and end positions
start_index = grid.index("S")
end_index   = grid.index("E")
startx = start_index % ncol
starty = start_index // ncol
endx   = end_index % ncol
endy   = end_index // ncol

grid = np.array(list(grid.replace("\n", ""))).reshape((nrow, ncol))

# Make sure start and end were found correctly
# print(grid[endy, endx])
# print(grid[starty, startx])

# Convert the array to numbers
def char_to_int(c):
    if c == "E": return 25
    elif c == "S": return 0
    else: return ord(c) - 97

grid = np.vectorize(char_to_int)(grid)

# print(np.min(grid))
# print(np.max(grid))

# Find all the locations that step upward 1 unit
class Step:
    def __init__(self, fromx, fromy, tox, toy):
        self.fromx = fromx
        self.fromy = fromy
        self.tox = tox
        self.toy = toy

steps = {i:list() for i in range(0,26)}

def get_if_inbounds(grid, x, y):
    if y >= 0 and y < nrow and x >= 0 and x < ncol:
        return grid[y, x]
    else:
        return -1

for i in range(ncol):
    for j in range(nrow):
        this_elev = grid[j, i]
        target_elev = grid[j, i] + 1
        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if get_if_inbounds(grid, j+dy, i+dx) == target_elev:
                steps[this_elev].append(Step(i, j, i+dx, j+dy))

print(sum(len(s) for s in steps.values()))

# Find which steps are reachable
stepdict = {
    'l': (-1,  0),
    'r': ( 1,  0),
    'u': ( 0, -1),
    'd': ( 0,  1)
}
def reachable(grid, x1, y1, x2, y2, path=[], current_min=None):
    # Determine shortest distance from (x1, y1) to (x2, y2)
    # or return nrow*ncol+1 if no such path exists

    # TODO these modifications
    #  - Once a path is found, memoize its length. Terminate any
    #       searches that exceed this length.
    #  - Prioritize movements that go towards the destination, only
    #       go away from destination if going towards it results in
    #       a dead end.
    
    # Initialize the min
    if current_min is None:
        current_min = grid.shape[0] * grid.shape[1] + 1

    # Add the current step to the path
    path.append((x1, y1))

    # If we have exceeded the current minimum distance, abort
    if len(path)-1 > current_min:
        path.pop()
        return grid.shape[0] * grid.shape[1] + 1

    # Check if the end was found
    if x1 == x2 and y1 == y2:
        print("Found destination")
        return len(path) - 1 # ignore starting square
    
    # Prioritize steps that go towards the destination
    priority_x = "rl" if x2 - x1 > 0 else "lr"
    priority_y = "du" if y2 - y1 > 0 else "ud"
    if abs(x2 - x1) > abs(y2 - y1):
        priority = priority_x[0] + priority_y[0] + priority_y[1] + priority_x[1]
    else:
        priority = priority_y[0] + priority_x[0] + priority_x[1] + priority_y[1]
    
    steps = [stepdict[p] for p in priority]

    # Determine which steps are valid
    # A step is valid if it does not gain elevation and has not
    # been seen before.
    valid_steps = [
        (dx, dy) for (dx, dy) in steps 
        if get_if_inbounds(grid, x1+dx, y1+dy) == grid[y1, x1] and
        get_if_inbounds(grid, x1+dx, y1+dy) != -1 and
        (x1+dx, y1+dy) not in path
    ]

    print("(x1, y1) = ({}, {})".format(x1, y1))
    print("(x2, y2) = ({}, {})".format(x2, y2))
    print("Priority:", steps)
    print()

    if len(valid_steps) == 0:
        # No valid steps found
        path.pop()
        return grid.shape[0] * grid.shape[1] + 1

    for (dx, dy) in valid_steps:
        current_min = min(
            current_min,
            reachable(grid, x1+dx, y1+dy, x2, y2, path, current_min)
        )

    # Pop this step from the path before going back up a level
    # in the call stack
    path.pop()

    return current_min

path = []
print(reachable(grid, 6, 0, 34, 2, path))  