from itertools import combinations

lines = list(map(lambda x: int(x.strip()), list(open("d1_input.txt"))))

for c in combinations(lines, 2):
    if sum(c) == 2020:
        print(c[0] * c[1])
        break

for c in combinations(lines, 3):
    if sum(c) == 2020:
        print(c[0] * c[1] * c[2])
        break