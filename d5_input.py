lines = map(lambda x: x.strip(), open("d5_input.txt"))

def binary_partition(lower, upper, lowchar, highchar, line):
    for char in line:
        if char == lowchar: # keep front
            upper = upper - ((upper-lower) // 2) - 1
        elif char == highchar: # keep back
            lower = lower + ((upper-lower) // 2) + 1
    return lower # == upper

seen_ids = []
for line in lines:
    row = binary_partition(0, 127, "F", "B", line[:8])
    col = binary_partition(0, 7, "L", "R", line[-3:])
    seat_id = row * 8 + col
    seen_ids.append(seat_id)

seen_ids.sort()
for i in range(0, len(seen_ids)-1):
    delta = seen_ids[i+1] - seen_ids[i]
    if delta != 1: print(seen_ids[i:i+2])