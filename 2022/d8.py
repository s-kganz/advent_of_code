from tkinter import dnd
import numpy as np

small_input = '''30373
25512
65332
33549
35390'''

#arr = np.array([np.array(list(map(int, line))) for line in small_input.split("\n")])
arr = np.array([np.array(list(map(int, line.strip()))) for line in open("2022/d8_input.txt").readlines()])

# Part 1 - how many trees are visible?
# column-wise max N -> S
ns_max = np.maximum.accumulate(arr)
# row-wise max W -> E
we_max = np.maximum.accumulate(arr, axis=1)
# column-wise max S -> N
sn_max = np.flip(np.maximum.accumulate(np.flip(arr)))
# row-wise max E -> W
ew_max = np.flip(np.maximum.accumulate(np.flip(arr), axis=1))

# Shift maxima 1-cell in the viewing direction, fill the values
# that wrap around with zeros. Note this only works with the
# interior trees.
ns_roll = np.roll(ns_max, 1, 0)
ns_roll[0, :] = 0

sn_roll = np.roll(sn_max, -1, 0)
sn_roll[-1, :] = 0

we_roll = np.roll(we_max, 1, 1)
we_roll[:, 0] = 0

ew_roll = np.roll(ew_max, -1, 1)
ew_roll[:, -1] = 0

interior_visible = np.logical_or.reduce((
    arr > ns_roll,
    arr > sn_roll,
    arr > we_roll,
    arr > ew_roll
))
exterior_cells = 2 * (arr.shape[0] + arr.shape[1] - 2)
print(
    "Number of trees visible: ", 
    exterior_cells + np.sum(interior_visible[1:-1, 1:-1])
)

# Part 2: what is the highest viewing score?
# no spicy numpy tricks here, just good ole for loops
def view_distance(a, i, j, dxn):
    start_value = a[i][j]
    loop_start = True
    count = 0
    while loop_start or start_value > a[i][j]:
        loop_start = False
        count += 1
        if dxn == "up": i -= 1
        if dxn == "dn": i += 1
        if dxn == "le": j -= 1
        if dxn == "ri": j += 1
        # check inbounds
        if (i >= a.shape[0] or j >= a.shape[1] or i < 0 or j < 0):
            count -= 1
            break
    return count

max_view_score = 0
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        view_score = \
            view_distance(arr, i, j, 'up') *\
            view_distance(arr, i, j, "dn") *\
            view_distance(arr, i, j, "le") *\
            view_distance(arr, i, j, "ri")
        max_view_score = max(max_view_score, view_score)

print("Max view score: ", max_view_score)
