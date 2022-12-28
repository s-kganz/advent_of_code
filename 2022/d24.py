# Following along with this solution by /u/Special_Freedom_8069
# https://pastebin.com/T2resb87

from collections import deque

# Movement constants
UP    = -1j
DOWN  =  1j
LEFT  = -1
RIGHT =  1
WAIT  =  0

MOVES = [UP, DOWN, LEFT, RIGHT, WAIT]

STORM_MOVE_DICT = {
    ">": RIGHT,
    "<": LEFT,
    "^": UP,
    "v": DOWN
}

class Storm:
    xmin = 0
    xmax = None
    ymin = 0
    ymax = None

    @classmethod
    def complex_modulo(cls, c):
        return complex(c.real % cls.xmax, c.imag % cls.ymax)

    def __init__(self, x, y, vector):
        self.pos = complex(x, y)
        self.vector = vector
    
    def position(self, time):
        return self.complex_modulo(self.pos + self.vector * time)
    
    def __repr__(self):
        return "Initial position: {}\tVector: {}".format(self.pos, self.vector)
    

def read_puzzle(fname):
    # Read in data
    storms = list()
    y = -1
    for line in map(str.strip, open(fname).readlines()):
        # Throw away the first line because it doesn't have any storms.
        if y == -1:
            # Determine xmin and xmax from length of line
            xmax = len(line) - 2
            y += 1
            continue

        # Read in actual storms
        for x in range(len(line)):
            if line[x] in STORM_MOVE_DICT:
                storms.append(Storm(x-1, y, STORM_MOVE_DICT[line[x]]))
        
        y += 1

    # Set the max y-coordinate
    ymax = y-1

    # Calculate the start and end positions
    start = 0 - 1j
    end   = xmax-1 + (ymax)*1j

    return storms, start, end, xmax, ymax

def hash_storm_map(storm_map):
    return hash(tuple(storm_map))

def generate_storm_map(storms, time_step):
    # Return as a set so we can get O(1) lookup
    # of a position that possibly has a storm.
    return set(map(
        lambda x: x.position(time_step), storms
    ))

def generate_all_storm_maps(storms):
    init_map = generate_storm_map(storms, 0)
    init_hash = hash_storm_map(init_map)
    maps = [init_map]
    i = 1
    while True:
        new_map = generate_storm_map(storms, i)
        if hash_storm_map(new_map) == init_hash:
            # storm pattern is now repeating
            print("Storms repeat at minute {}".format(i))
            break
        maps.append(new_map)
        i += 1
    return maps

def get_possible_moves(pos, time, storm_maps, xmax, ymax, start, end):
    # Get the map for the *next* time step
    storms = storm_maps[(time+1) % len(storm_maps)]
    candidate_moves = list(map(lambda c: pos+c, MOVES))
    allowed_moves = list(filter(
        lambda c: c in [start, end] or (
            0 <= c.real < xmax and
            0 <= c.imag < ymax and
            c not in storms
        ),
        candidate_moves
    ))
    return allowed_moves

def breadth_first_path_search(start, end, init_time, storm_maps, xmax, ymax):
    Q = deque()
    Q.append((start, init_time))

    while len(Q) != 0:
        cur_pos, cur_time = Q.popleft()

        if cur_pos == end:
            # print("Found end")
            return cur_pos, cur_time

        possible_moves = get_possible_moves(
            cur_pos, cur_time, storm_maps, xmax, ymax, start, end
        )

        for pm in possible_moves:
            if (pm, cur_time+1) not in Q:
                Q.append((pm, cur_time+1))
    
    raise Exception("Failed to find path to end :(")


storms, start, end, xmax, ymax = read_puzzle("2022/d24_input.txt")
Storm.xmax = xmax
Storm.ymax = ymax
# print(storms)
print("Starting position: ", start)
print("Ending position: ", end)
print("Xmax: ", xmax)
print("Ymax: ", ymax)
print("Generating storm maps...")
storm_maps = generate_all_storm_maps(storms)

end, time1 = breadth_first_path_search(start, end, 0, storm_maps, xmax, ymax)
print("Part 1: ", time1)

start, time2 = breadth_first_path_search(end, start, time1, storm_maps, xmax, ymax)
print("Returned to start after {} minutes".format(time2))

end, time3 = breadth_first_path_search(start, end, time2, storm_maps, xmax, ymax)
print("Returned to end after {} minutes".format(time3))
print("Part 2: ", time3)
