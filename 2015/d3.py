path = next(open("d3_input.txt")).strip()

seen = set()
sx, sy = 0, 0
rx, ry = 0, 0


def move(x, y, inst):
    if inst == "^": y += 1
    elif inst == "v": y -= 1
    elif inst == "<": x -= 1
    else: x += 1
    return x, y

move_s = True
for char in path:
    if move_s:
        sx, sy = move(sx, sy, char)
        seen.add((sx, sy))
    else:
        rx, ry = move(rx, ry, char)
        seen.add((rx, ry))
    move_s = not move_s
    
    

print(len(seen))