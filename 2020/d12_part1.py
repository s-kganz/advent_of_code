lines = list(map(lambda x: x.strip(), open("d12_input.txt")))

x, y = 0, 0
dirxn = 1 # 0, 1, 2, 3 == N, E, S, W
dirxns = ["N", "E", "S", "W"]
for inst in lines:
    letter, value = inst[0], int(inst[1:])
    # determine if a turn needs to happen
    if letter == "F": letter = dirxns[dirxn]
    elif letter == "L":
        dirxn = (dirxn - (value // 90)) % 4
        continue
    elif letter == "R":
        dirxn = (dirxn + (value // 90)) % 4

    if letter == 'N':
        y += value
    elif letter == "S":
        y -= value
    elif letter == "E":
        x += value
    elif letter == "W":
        x -= value

print(abs(x) + abs(y))