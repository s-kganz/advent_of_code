program = map(str.strip, open("2022/d10_input.txt").readlines())

reg = 1
ticks = 0

checks = [20, 60, 100, 140, 180, 220]
checksum = 0
px_per_row = 40
n_rows = 6
crt = [0] * (px_per_row * n_rows)

def update():
    global ticks, reg, checksum, ticks
    ticks += 1
    px_pos = (ticks-1) % px_per_row
    crt[ticks-1] = "#" if abs(px_pos-reg) < 2 else "."
    if ticks in checks:
        checksum += reg * ticks

for line in program:
    do_add = line[0] != "n"
    update()
    if do_add:
        # draw happens before add
        update()
        reg += int(line.split(" ")[1])

print("Part 1:", checksum)
print("Part 2:")     
for i in range(len(crt)):
    print(crt[i], end="")
    if (i+1) % 40 == 0:
        print()
