import math

lines = list(map(lambda x: x.strip(), open("d12_input.txt")))

boatx, boaty = 0, 0
ptx, pty = 10, 1
dirxn = 1 # 0, 1, 2, 3 == N, E, S, W
dirxns = ["N", "E", "S", "W"]
for inst in lines:
    letter, value = inst[0], int(inst[1:])
    if letter == "F": 
        boatx += (ptx * value)
        boaty += (pty * value)
    elif letter in "RL":
        if letter == "R": value = 360 - value
        rads = value * math.pi / 180
        newx = round((ptx * math.cos(rads)) - (pty * math.sin(rads)))
        newy = round((ptx * math.sin(rads)) + (pty * math.cos(rads)))
        ptx, pty = newx, newy

    elif letter == 'N':
        pty += value
    elif letter == "S":
        pty -= value
    elif letter == "E":
        ptx += value
    elif letter == "W":
        ptx -= value

print(abs(boatx) + abs(boaty))