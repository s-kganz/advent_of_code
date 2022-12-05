with open("2022/d4_input.txt") as file:
    lines = file.readlines()

n_contained = 0
for line in lines:
    ranges = line.strip().split(",")
    r1_lower, r1_upper = tuple(map(int, ranges[0].split("-")))
    r2_lower, r2_upper = tuple(map(int, ranges[1].split("-")))

    # Part 1
    '''
    if r2_lower <= r1_lower and r2_upper >= r1_upper:
        n_contained += 1
        continue
    elif r1_lower <= r2_lower and r1_upper >= r2_upper:
        n_contained += 1
        continue
    '''

    # Part 2
    if not (r1_upper < r2_lower or r2_upper < r1_lower):
        n_contained += 1
        continue

print(n_contained)