tiles = dict()
deltas = {
    'e': (2, 0),
    'w': (-2, 0),
    'ne': (1, 1),
    'se': (1, -1),
    'nw': (-1, 1),
    'sw': (-1, -1)
}

lines = map(str.strip, open("d24_input.txt"))

for line in lines:
    x, y = 0, 0
    i = 0
    while i < len(line):
        if line[i] in "ns":
            move = line[i:i+2]
            i+=1
        else:
            move = line[i]
        delta = deltas[move]
        x += delta[0]
        y += delta[1]

        i += 1
    if (x, y) in tiles:
        tiles[(x, y)] = not tiles[(x, y)]
    else:
        tiles[(x, y)] = True

print(sum(tiles.values())) # part 1

xcoords = list(tup[0] for tup in tiles.keys())
ycoords = list(tup[1] for tup in tiles.keys())
minx, maxx = min(xcoords), max(xcoords)
miny, maxy = min(ycoords), max(ycoords)

def do_cycle(oldfloor, minx, maxx, miny, maxy):
    newfloor = dict()
    # check every valid coordinate within the bounding box
    # include upper bounds
    for x in range(minx-2, maxx+3):
        for y in range(miny-1, maxy+2):
            if not (x % 2) == (y % 2): continue
            # count the neighbors
            neighbors = 0
            for delta in deltas.values():
                newx, newy = x+delta[0], y+delta[1]
                if (newx, newy) in oldfloor and oldfloor[(newx, newy)]:
                    neighbors += 1

            if (x, y) in oldfloor:
                if oldfloor[(x, y)] and (neighbors == 0 or neighbors > 2):
                    newfloor[(x, y)] = False
                elif (not oldfloor[(x, y)]) and neighbors == 2:
                    newfloor[(x, y)] = True
                else:
                    newfloor[(x, y)] = oldfloor[(x, y)]
            # this tile must be in the default state
            elif neighbors == 2:
                newfloor[(x, y)] = True
                maxx = max(maxx, x)
                minx = min(minx, x)
                maxy = max(maxy, y)
                miny = min(miny, y)

    return newfloor, minx, maxx, miny, maxy

for _ in range(100):
    tiles, minx, maxx, miny, maxy = do_cycle(tiles, minx, maxx, miny, maxy)


print(sum(tiles.values()))

