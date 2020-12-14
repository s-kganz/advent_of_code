import numpy as np

# part1
'''
board = np.zeros((1000, 1000), dtype="bool")

for inst in map(str.strip, open("d6_input.txt")):
    tokens = inst.split(" ")
    if len(tokens) == 4: # toggle
        c1 = tuple(map(int, tokens[1].split(",")))
        c2 = tuple(map(int, tokens[3].split(",")))

        np.invert(board[c1[0]:c2[0]+1, c1[1]:c2[1]+1], out=board[c1[0]:c2[0]+1, c1[1]:c2[1]+1])
    if len(tokens) == 5: # turn on/off
        new_val = 1 if tokens[1] == "on" else 0
        c1 = tuple(map(int, tokens[2].split(",")))
        c2 = tuple(map(int, tokens[4].split(",")))
        board[c1[0]:c2[0]+1, c1[1]:c2[1]+1] = int(new_val)
'''
#part2
board = np.zeros((1000, 1000), dtype="int")
for inst in map(str.strip, open("d6_input.txt")):
    tokens = inst.split(" ")
    if len(tokens) == 4: # toggle
        c1 = tuple(map(int, tokens[1].split(",")))
        c2 = tuple(map(int, tokens[3].split(",")))

        board[c1[0]:c2[0]+1, c1[1]:c2[1]+1] += 2
    if len(tokens) == 5: # turn on/off
        new_val = 1 if tokens[1] == "on" else -1
        c1 = tuple(map(int, tokens[2].split(",")))
        c2 = tuple(map(int, tokens[4].split(",")))
        board[c1[0]:c2[0]+1, c1[1]:c2[1]+1] += new_val
    
    board[board < 0] = 0

print(np.sum(board))