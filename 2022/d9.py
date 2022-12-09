import numpy as np

small_input = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

pos = set()
movedict = {
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
    "L": np.array([-1, 0]),
    "R": np.array([1, 0])
}

# Part 1
'''
t = np.array([0, 0])
h = np.array([0, 0])
#for line in map(str.strip, small_input.split("\n")):
for line in map(str.strip, open("2022/d9_input.txt").readlines()):
    # do the move
    dxn, dist = line.split(" ")[0], int(line.split(" ")[1])
    move = movedict[dxn]
    for _ in range(dist):
        # apply the movement to the head
        h += move
        if not np.all(np.abs(h - t) < 2):
            # Tail needs to update - always goes
            # one unit behind the head in dirxn of
            # movement
            t = h - move
        pos.add(",".join(map(str, t)))
            
print("Tail positions visited:", len(pos))
'''

# Part 2 - ten knots now!
# For each move
#   update the head
#   for each knot
#       update the knot according to the
#        next upstream knot

small_input_2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''

def update_knot_position(h, t, last_move):
    if not np.all(np.abs(h - t) < 2):
        # Tail needs to update
        dx, dy = tuple(h - t)
        movex, movey = (dx != 0) * np.sign(dx), (dy != 0) * np.sign(dy)
        return t + np.array([movex, movey]) 
    else:
        # no update needed
        return t

n_knots = 10
rope = np.repeat(0, n_knots*2).reshape((n_knots, 2))

for line in map(str.strip, open("2022/d9_input.txt").readlines()):
#for line in map(str.strip, small_input_2.split("\n")):
    dxn, dist = line.split(" ")[0], int(line.split(" ")[1])
    move = movedict[dxn]
    for _ in range(dist):
        # Apply the move directly only to the head knot
        rope[0] += move
        # Subsequent knots are updated according to the
        # next upstream knot
        for i in range(rope.shape[0]-1):
            rope[i+1] = update_knot_position(rope[i], rope[i+1], move)
        # Record position of tail
        pos.add(",".join(map(str, rope[-1, :])))

print("Number of positions visited:", len(pos))