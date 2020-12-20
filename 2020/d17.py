from copy import deepcopy

hypercube = [[list(map(
    lambda L: [1 if char == "#" else 0 for char in L.strip()], 
    open("d17_input.txt"))
)]]

def pad_w(hypercube, front=False):
    planes = len(hypercube[0])
    rows = len(hypercube[0][0])
    cols = len(hypercube[0][0][0])
    cube = [
        [[0] * rows for _ in range(cols)] for _ \
            in range(planes)
    ]
    if front:
        hypercube.insert(0, cube)
    else:
        hypercube.append(cube)

def pad_z(hypercube, above=False):
    # get the dimensions of the plane
    rows = len(hypercube[0][0])
    cols = len(hypercube[0][0][0])
    for i in range(len(hypercube)):
        plane = [[0] * rows for _ in range(cols)]
        if above:
            hypercube[i].insert(0, plane)
        else:
            hypercube[i].append(plane)

def pad_x(hypercube, left=False):
    for cube in hypercube:
        for plane in cube:
            for row in plane:
                if left:
                    row.insert(0, 0)
                else:
                    row.append(0)

def pad_y(hypercube, top=False):
    for cube in hypercube:
        for plane in cube:
            row = [0] * len(plane[0])
            if top:
                plane.insert(0, row)
            else:
                plane.append(row)

def coords_valid(cube, w, x, y, z):
    if not 0 <= w < len(cube): return False
    if not 0 <= x < len(cube[w]): return False
    if not 0 <= y < len(cube[w][x]): return False
    if not 0 <= z < len(cube[w][x][y]): return False
    return True

def count_neighbors(hypercube, w, x, y, z):
    neighbors = 0
    delta = [-1, 0, 1]
    for dw in delta:
        for dx in delta:
            for dy in delta:
                for dz in delta:
                    if not (dx == dy == dz == dw == 0) and \
                    coords_valid(hypercube, dw+w, dx+x, dy+y, dz+z) and \
                    hypercube[w+dw][x+dx][dy+y][dz+z]:
                        neighbors += 1
    return neighbors

def do_cycle(cube):
    new_cube = list()
    do_padding = [False] * 8
    for i in range(len(cube)): # w
        new_cube.append(list())
        for j in range(len(cube[i])): # z
            new_cube[i].append(list())
            for k in range(len(cube[i][j])): # y
                new_cube[i][j].append(list())
                for l in range(len(cube[i][j][k])): # x
                    neighbors = count_neighbors(cube, l, k, j, i)
                    became_active = False
                    if cube[i][j][k][l]:
                        new_cube[i][j][k].append(int(neighbors in (2, 3)))
                    elif neighbors == 3:
                        became_active = True
                        new_cube[i][j][k].append(1)
                    else:
                        new_cube[i][j][k].append(0)

                    if became_active:
                        if i == 0: do_padding[0] = True
                        if i == len(cube)-1: do_padding[1] = True
                        if j == 0: do_padding[2] = True
                        if j == len(cube[i])-1: do_padding[3] = True
                        if k == 0: do_padding[4] = True
                        if k == len(cube[i][j])-1: do_padding[5] = True
                        if l == 0: do_padding[6] = True
                        if l == len(cube[i][j][k]): do_padding[7] = True

    if do_padding[0]: pad_w(new_cube, front=True)
    if do_padding[1]: pad_w(new_cube, front=False)
    if do_padding[2]: pad_z(new_cube, above=True)
    if do_padding[3]: pad_z(new_cube, above=False)
    if do_padding[4]: pad_y(new_cube, top=True)
    if do_padding[5]: pad_y(new_cube, top=False)
    if do_padding[6]: pad_x(new_cube, left=True)
    if do_padding[7]: pad_x(new_cube, left=False)
      
    return new_cube

def print_cube(cube):
    strs = map(lambda plane: "\n".join(str(row) for row in plane), cube)
    print("\n---\n".join(strs))

def sum_cube(cube):
    tot = 0
    for i in range(len(cube)):
        for j in range(len(cube[i])):
            for k in range(len(cube[i][j])):
                for l in range(len(cube[i][j][k])):
                    if cube[i][j][k][l]: tot += 1
    return tot

pad_w(hypercube, True)
pad_w(hypercube, False)
pad_z(hypercube, True)
pad_z(hypercube, False)
pad_y(hypercube, True)
pad_y(hypercube, False)
pad_x(hypercube, True)
pad_x(hypercube, False)

for _ in range(6):
    hypercube = do_cycle(hypercube)

print(sum_cube(hypercube))