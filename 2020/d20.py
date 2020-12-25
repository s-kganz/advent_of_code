import numpy as np
import regex as re

f = "".join(open("d20_input.txt")).split("\n\n")
tiles = dict()
tilehashes = dict()
tilenums = list()
neighbors = dict()

def make_hash(s):
    s_both = (s, s[::-1])
    return eval("0b" + min(s_both) + max(s_both))

# Read the tiles and hash the edges
for tile in f:
    lines = tile.split("\n")[1:]
    tilenum = int(tile[tile.index(" ")+1:tile.index(":")])
    tilenums.append(tilenum)
    hashes = [
        make_hash("".join("1" if c == "#" else "0" for c in lines[0])),
        make_hash("".join("1" if c == "#" else "0" for c in lines[-1])),
        make_hash("".join("1" if line[0] == "#" else "0" for line in lines)),
        make_hash("".join("1" if line[-1] == "#" else "0" for line in lines))
    ]
    for h in hashes:
        if h in tilehashes:
            tilehashes[h].append(tilenum)
        else:
            tilehashes[h] = [tilenum]
    tilearr = [list(1 if c == "#" else 0 for c in line) for line in lines]
    tiles[tilenum] = np.array(tilearr)

# Determine the neighbor relationships
for lis in tilehashes.values():
    for i in range(len(lis)):
        lis_subset = lis[0:i] + lis[i+1:]
        if lis[i] not in neighbors:
            neighbors[lis[i]] = set()
        for num in lis_subset:
            neighbors[lis[i]].add(num)

# Build the board
n = int(pow(len(tilenums), 0.5))
board = np.zeros(n * n).reshape((n, n))

def match_horiz(left, right):
    return list(s[-1] for s in tiles[left]) == list(s[0] for s in tiles[right])

def match_vert(top, bottom):
    return all(tiles[top][-1] == tiles[bottom][0])

# Recursively add on to the image
seed = next(num for num in tilenums if len(neighbors[num]) == 2)
board[0][0] = seed
on_board = {seed}

def find_match(tilenum, orient='vertical'):
    match_func = match_vert if orient == "vertical" else match_horiz
    flipax = 0 if orient == "horizontal" else 1
    candidates = neighbors[tilenum]
    for num in candidates:
        if num in on_board: continue
        for _ in range(4):
            if match_func(tilenum, num):
                return num
            tiles[num] = np.rot90(tiles[num])    
        tiles[num] = np.flip(tiles[num], axis=flipax)
        for _ in range(4):
            if match_func(tilenum, num):
                return num
            tiles[num] = np.rot90(tiles[num])
        tiles[num] = np.flip(tiles[num]) # return to original state
    return None

# driver for orienting the first tile
def setup(tilenum):
    for _ in range(4):
        if find_match(seed, "vertical") is not None and \
        find_match(seed, "horizontal") is not None:
            return True
        tiles[seed] = np.rot90(tiles[seed])
    return False

if not setup(seed):
    tiles[seed] = np.flip(tiles[seed])
    assert(setup(seed))

for row in range(len(board)):
    for col in range(len(board)):
        if board[row][col] == 0: continue
        if col+1 < len(board):
            result = find_match(board[row][col], "horizontal")
            if result is not None:
                board[row][col+1] = result
                on_board.add(result)
        if row+1 < len(board):
            result = find_match(board[row][col], "vertical")
            if result is not None:
                board[row+1][col] = result
                on_board.add(result)

# the image is now assembled
# answer to part 1
print(board[0][0] * board[-1][0] * board[0][-1] * board[-1][-1])

# strip the borders
for key in tiles:
    tiles[key] = tiles[key][1:-1, 1:-1]

# create the full image in a single matrix
# turn into a string so we can use regex
image = None
for row in range(len(board)):
    image_row = tiles[board[row][0]]
    for col in range(1, len(board)):
        image_row = np.hstack((image_row, tiles[board[row][col]]))
    if image is None: 
        image = image_row
    else:
        image = np.vstack((image, image_row))
imagestr = "".join(map(str, image.flatten()))

# no one ever said she was pretty
monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
monstarr = np.array(list(map(
    lambda line: [1 if char == "#" else 0 for char in line], 
    monster.split("\n")
)))
monster_hash = 15

def build_regex(arr, img_width):
    regex_lines = ["".join(map(str, row)).replace("0", ".") for row in arr]
    dot_count = img_width - len(regex_lines[0])
    regex = ".{{{}}}".format(dot_count).join(regex_lines)
    return re.compile(regex)

regexes = []
for _ in range(4):
    regexes.append(build_regex(monstarr, image.shape[0]))
    monstarr = np.rot90(monstarr)
monstarr = np.flip(monstarr, 1)
for _ in range(4):
    regexes.append(build_regex(monstarr, image.shape[0]))
    monstarr = np.rot90(monstarr)

for regex in regexes:
    matches = len(re.findall(regex, imagestr, overlapped=True))
    if matches > 0:
        print(np.sum(image) - matches * monster_hash)
