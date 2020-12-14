line = next(open("d1_input.txt")).strip()

floor = 0
i = 0
while i < len(line):
    if line[i] == "(": floor += 1
    else: floor -= 1
    if floor < 0: break
    i += 1

print(i)