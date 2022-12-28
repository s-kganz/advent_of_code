# Define movement transforms
MOVE_NORTH = lambda x: (x[0], x[1]-1)
MOVE_EAST  = lambda x: (x[0]+1, x[1])
MOVE_SOUTH = lambda x: (x[0], x[1]+1)
MOVE_WEST  = lambda x: (x[0]-1, x[1])

# Define neighbor transforms
NEIGHBOR_NORTH = lambda x: [(x[0]-1, x[1]-1), (x[0], x[1]-1), (x[0]+1, x[1]-1)]
NEIGHBOR_SOUTH = lambda x: [(x[0]-1, x[1]+1), (x[0], x[1]+1), (x[0]+1, x[1]+1)]
NEIGHBOR_EAST  = lambda x: [(x[0]+1, x[1]+1), (x[0]+1, x[1]), (x[0]+1, x[1]-1)]
NEIGHBOR_WEST  = lambda x: [(x[0]-1, x[1]+1), (x[0]-1, x[1]), (x[0]-1, x[1]-1)]

# Combine movement and neighbor transforms so they can be reordered
# together.
MOVE_ORDER = [
    (MOVE_NORTH, NEIGHBOR_NORTH),
    (MOVE_SOUTH, NEIGHBOR_SOUTH),
    (MOVE_WEST, NEIGHBOR_WEST),
    (MOVE_EAST, NEIGHBOR_EAST)
]

def propose_move(pos, elves):
    x, y = pos
    # Determine the next position for this elf
    neighbors_present = list(map(
        lambda move: any(t in elves for t in move[1]((x, y))),
        MOVE_ORDER
    ))
    if all(np == False for np in neighbors_present):
        # No neighbors in 8-neighborhood, do not move
        return (x, y)
    
    i = 0
    while i < len(MOVE_ORDER):
        if not neighbors_present[i]:
            # Propose to move to this position
            return MOVE_ORDER[i][0]((x, y))
        i += 1 
    # No moves are possible
    return x, y

# Read in data
char_elf = '#'
char_blank = '.'
elves = set()
y = 0
for line in open("2022/d23_input.txt").readlines():
    for x in range(len(line.strip())):
        if line[x] == char_elf:
            elves.add((x, y))
    y += 1

# Part 1
# n_rounds = 10
# for _ in range(n_rounds):
# Part 2
round_number = 1
while True:
    # Propose new positions
    seen_pos = set()
    duplicate_pos = set()
    elves_proposed = dict()
    for e in elves:
        e_p = propose_move(e, elves)
        if e_p in seen_pos: duplicate_pos.add(e_p)
        seen_pos.add(e_p)
        elves_proposed[e] = e_p
    elves_new = set()
    elf_moved = False
    for key in elves_proposed:
        if elves_proposed[key] in duplicate_pos:
            # Write original position due to collision
            elves_new.add(key)
        else:
            # Write new position
            elves_new.add(elves_proposed[key])
            if elves_proposed[key] != key:
                elf_moved = True
    if not elf_moved:
        break
    # Update the position set
    elves = elves_new

    # Update the direction order
    MOVE_ORDER = MOVE_ORDER[1:] + [MOVE_ORDER[0]]

    # Increment the number of rounds
    round_number += 1

# Determine the minimum bounding rectangle for the elves
xmin = min(e[0] for e in elves)
xmax = max(e[0] for e in elves)
ymin = min(e[1] for e in elves)
ymax = max(e[1] for e in elves)
ntiles = (xmax - xmin + 1) * (ymax - ymin + 1)
nempty = ntiles - len(elves)

print("Rounds elapsed: {}".format(round_number))
print("X range: {} - {}, Y range: {} - {}".format(xmin, xmax, ymin, ymax))
print("Number of empty tiles: {}".format(nempty))