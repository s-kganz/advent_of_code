BOARD_wIDTH = 7

# Represent the rocks as bitmasks
ROCKS = [
    # Line
    lambda y: {y: 0b0011110},
    # Plus sign
    lambda y: {y: 0b0001000, y+1: 0b0011100, y+2: 0b0001000},
    # Backwards L
    lambda y: {y: 0b0011100, y+1: 0b0000100, y+2: 0b0000100},
    # I
    lambda y: {y: 0b0010000, y+1: 0b0010000, y+2: 0b0010000, y+3: 0b0010000},
    # Box
    lambda y: {y: 0b0011000, y+1: 0b0011000}
]

def move_right(rock):
    # If the zero-th bit is not set anywhere, shift 1 to the right
    # in place.
    out = {}
    if all(v & 1 == 0 for v in rock.values()):
        out = {}
        for key in rock:
            out[key] = rock[key] >> 1
        return out
    return rock
    
def move_left(rock):
    # If the BOARD_WIDTH-th bit is not set anywhere, shift 1 to
    # the left.
    if all(v & (1 << (BOARD_wIDTH-1)) == 0 for v in rock.values()):
        out = {}
        for key in rock:
            out[key] = rock[key] << 1
        return out
    return rock

def move_up(rock):
    # Shift all the keys to be at y+1
    out = {}
    for y in rock:
        out[y+1] = rock[y]
    return out

def move_down(rock):
    # Shift all the keys to be at y-1
    out = {}
    for y in rock:
        out[y-1] = rock[y]
    return out

MOVE_REVERSE = {
    move_left: move_right,
    move_right: move_left,
    move_up: move_down,
    move_down: move_up
}

def collision(board, rock):
    # Determine if the board and rock collide with each other
    min_y = max(0, min(rock.keys()))
    max_y = min(len(board)-1, max(rock.keys()))
    for y in range(min_y, max_y+1):
        if board[y] & rock[y]:
            return True
    return False

def write_rock(board, rock):
    # Possibly append zeros if the board needs to expand upward
    if len(board)-1 < max(rock.keys()):
        board.extend([0] * (max(rock.keys()) - len(board) + 1))
    for key in rock:
        board[key] |= rock[key]

def print_rock(rock):
    for y in range(max(rock.keys()), min(rock.keys())-1, -1):
        print("{:4}: {:07b}".format(y, rock[y]))

def print_board(board):
    for y in range(len(board)-1, -1, -1):
        print("{:4}: |{:07b}|".format(y, board[y]))

def read_puzzle(fname):
    return open(fname).read().strip()

def drop_rock(board, rock, jets, jet_idx):
    while True:
        # Apply the jet movement
        rock_jet = jets[jet_idx](rock)
        jet_idx = (jet_idx+1) % len(jets)
        if not collision(board, rock_jet):
            rock = rock_jet
        # Apply movement by gravity
        rock_down = move_down(rock)
        if collision(board, rock_down):
            # No further movements are possible
            break
        else:
            rock = rock_down
        
    # Rock has reached final position, write it
    write_rock(board, rock)
    return jet_idx

def simulate_rocks(board, jets, n_to_add):
    jet_idx = 0
    rock_idx = 0
    for _ in range(n_to_add):
        spawn_height = len(board) + 3
        rock = ROCKS[rock_idx](spawn_height)
        jet_idx = drop_rock(board, rock, jets, jet_idx)
        rock_idx = (rock_idx + 1) % len(ROCKS)

    return jet_idx, rock_idx

def find_dy_period(board, jets, jet_idx=0, rock_idx=0, window_size=10):
    # Continue adding rocks to the board until a repeat in the pattern
    # of *changes in height* is found. Returns repeat period and total.
    dy = []
    initial_y = len(board)
    n_rocks = 0
    while True:
        old_y = len(board)
        spawn_height = len(board) + 3
        rock = ROCKS[rock_idx](spawn_height)
        jet_idx = drop_rock(board, rock, jets, jet_idx)
        new_y = len(board)
        dy.append(new_y - old_y)
        rock_idx = (rock_idx + 1) % len(ROCKS)
        n_rocks += 1

        if len(dy) > window_size:
            if all(x == y for x, y in zip(dy[:window_size], dy[-window_size:])):
                # Found the pattern!
                repeat_period = len(dy) - window_size
                repeat_height = sum(dy[:-(window_size)])
                return repeat_period, repeat_height

jet_pattern = [
    move_right if c == '>' else move_left for c in read_puzzle("2022/d17_input.txt")
]

init_board = [
    # make a floor so we can detect a collision to start
    2 ** (BOARD_wIDTH) - 1
]

# Part 1
part1_sim_length = 2022
jet, rock = simulate_rocks(init_board, jet_pattern, part1_sim_length)
part1_sim_height = len(init_board)-1
print("Height after simulation: ", part1_sim_height)

# Part 2
part2_sim_length = 1000000000000
# We need to find a repeat in the pattern of *changes in y* as rocks
# are added to the tower.
window_size = 50
# Copy the board so we don't affect the current simulation.
repeat_period, repeat_height = find_dy_period(init_board.copy(), jet_pattern, jet, rock)
print("Found repeat after {} rocks".format(repeat_period))

rocks_remaining = part2_sim_length - part1_sim_length
repeats_remaining = rocks_remaining // repeat_period
rocks_remaining_after_repeats = rocks_remaining % repeat_period
height_from_repeats = repeats_remaining * repeat_height

# Simulate the remaining rocks
jet, rock = simulate_rocks(init_board, jet_pattern, rocks_remaining_after_repeats-2)
height_after_repeats = len(init_board)-1 - part1_sim_height

# Calculate final height
final_height = part1_sim_height + height_from_repeats + height_after_repeats

print("Height after simulation: ", final_height)
