def sign(x):
    if x > 0: return 1
    if x < 0: return -1
    else: return 0

blocks = dict()
for line in map(str.strip, open("2022/d14_input.txt").readlines()):
    points = list(map(lambda x: list(map(int, x.split(","))), line.split(" -> ")))
    for i in range(len(points)-1):
        dx, dy = sign(points[i+1][0] - points[i][0]), sign(points[i+1][1] - points[i][1])
        x, y = points[i][0], points[i][1]
        if x not in blocks: blocks[x] = set()
        blocks[x].add(y)
        while x != points[i+1][0] or y != points[i+1][1]:
            x += dx
            y += dy
            if x not in blocks: blocks[x] = set()
            blocks[x].add(y)

floor_y = 0
for key in blocks:
    blocks[key] = sorted(list(blocks[key]))
    floor_y = max(floor_y, blocks[key][-1])
# Part 2
floor_y += 2

# construct a hash table of the next available y coordinate
nexty = dict()
for key in blocks.keys():
    nexty[key] = {y:floor_y-1 for y in range(floor_y+1)}
    # Part 2: make a floor
    nexty[key][floor_y] = -1
    block_idx = 0
    for y in range(floor_y+1):
        if y > blocks[key][block_idx]: block_idx += 1
        if block_idx >= len(blocks[key]): break

        if y == blocks[key][block_idx]:
            nexty[key][y] = -1 # space is occupied
        else:
            nexty[key][y] = blocks[key][block_idx]-1

#for key in sorted(list(nexty.keys())):
#    print(key, nexty[key])

def get_nexty(x, y, nexty):
    # Returns the next y-coordinate for sand at (x, y) or None
    # if the coordinates are out of bounds
    if x not in nexty:
        nexty[x] = {y:floor_y-1 for y in range(floor_y+1)}
        # Part 2: make a floor
        nexty[x][floor_y] = -1
    if y not in nexty[x]: 
        return None
    return nexty[x][y]

def update_nexty(x, y, nexty):
    # Sets the coordinate (x, y) to occupied and updates
    # the next y-coordinate of unoccupied cells above
    # until an occupied one is found.
    nexty[x][y] = -1
    fill_value = y-1
    y -= 1
    while y >= 0 and nexty[x][y] != -1:
        nexty[x][y] = fill_value
        y -= 1


def next_position(insx, insy, nexty, path):
    # Find the resting position of sand
    newx, newy = insx, get_nexty(insx, insy, nexty)
    if newy == -1:
        # space is occupied, insertion not possible
        return -1, -1
    
    if newx is None or newy is None:
        # sand is falling into the void
        return None, None

    if (newx, newy) != path[-1]:
        path.append((newx, newy))

    # attempt to insert left
    leftx, lefty = next_position(newx-1, newy+1, nexty, path)
    # if y coordinate is valid and lower, accept it
    if lefty is None or lefty > newy:
        return leftx, lefty
    
    # attempt to insert right
    rightx, righty = next_position(newx+1, newy+1, nexty, path)
    # if y coordinate is valid and lower, accept it
    if righty is None or righty > newy:
        return rightx, righty
    
    # first coordinate is accepted
    return newx, newy

srcx = 500
srcy = 0
path = [(srcx, srcy)]

i = 0
while True:
    #print("Inserting at ({}, {})".format(path[-1][0], path[-1][1]))
    x, y = next_position(path[-1][0], path[-1][1], nexty, path)
    # print("Placed at ({}, {})".format(x, y))
    # Part 1
    # if x == None and y == None:
    # Part 2
    if x == srcx and y == srcy:
        break
    # print("{}: Sand fell at ({}, {})".format(i, x, y))
    update_nexty(x, y, nexty)
    path.pop()
    i += 1

# Part 1
# print("Sand fell into the void after {} ticks".format(i))
# Part 2
print("Reached source after {} ticks".format(i+1))