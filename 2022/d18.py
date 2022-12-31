from collections import deque
import numpy as np
from scipy.signal import convolve

def read_puzzle(fname):
    points = []
    with open(fname) as f:
        for line in f:
            points.append(tuple(map(int, line.strip().split(","))))
    
    return points

def array_inbounds(p, arr):
    for i in range(len(p)):
        if not 0 <= p[i] < arr.shape[i]:
            return False
    return True

def flood_fill(arr, p_init=None):
    if p_init is None:
        p_init = tuple([0] * len(arr.shape))
    
    arr_fill = np.zeros(arr.shape)
    arr_fill[p_init] = 1

    seen_points = set()
    queue = deque()
    seen_points.add(p_init)
    queue.append(p_init)
    while len(queue) > 0:
        p = queue.popleft()
        # Accept point if it is inbounds and equal to zero in the array
        if array_inbounds(p, arr) and arr[p] == 0:
            arr_fill[p] = 1
            # Generate neighbors and append to queue if they are inbounds
            # and have not been seen before.
            for dx, dy, dz in (
                (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
            ):
                p_new = p[0]+dx, p[1]+dy, p[2]+dz
                if array_inbounds(p_new, arr) and (p_new not in seen_points):
                    queue.append(p_new)
                    seen_points.add(p_new)
    return arr_fill

points = read_puzzle("2022/d18_input.txt")

# All the coordinates are positive, so the array shape is the max
# value on each axis
arr_shape = (
    max(p[0] for p in points)+1,
    max(p[1] for p in points)+1,
    max(p[2] for p in points)+1
)

obsid_present = np.zeros(arr_shape)

for p in points:
    obsid_present[p[0], p[1], p[2]] = 1

# Pad the array for the convolution to work properly
obsid_present = np.pad(obsid_present, 1)

surface_area_kernel = np.array([
    [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
])

n_neighbors = convolve(obsid_present, surface_area_kernel, mode="same")

n_sides = np.sum(
    n_neighbors[obsid_present == 0]
)

print("Part 1:", n_sides)

# (0, 0, 0) will always be outside the sphere because of zero padding.
is_outside = flood_fill(obsid_present, (0, 0, 0))

n_sides_outside = np.sum(
    n_neighbors[is_outside == 1]
)

print("Part 2:", n_sides_outside)
