small_input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

box_start, moves = tuple(open("2022/d5_input.txt").read().split("\n\n"))
#box_start, moves = tuple(small_input.split("\n\n"))

n_stacks = 9

stacks = [list() for x in range(n_stacks)]

for line in box_start.split("\n")[:-1]: # ignore numbers
    #print(line)
    boxes = line[:-1][1::4] # ignore trailing newline
    for i in range(len(boxes)):
        if boxes[i] != " ":
            stacks[i].append(boxes[i])

# get the stacks in lifo order
for s in stacks: s.reverse()

# apply all the moves
for move in map(str.strip, moves.split("\n")[:-1]):
    tokens = move.split(" ")
    n_moves = int(tokens[1])
    source  = int(tokens[3])
    dest    = int(tokens[5])
    
    # Part 1
    #for _ in range(n_moves):
    #    stacks[dest-1].append(stacks[source-1].pop())

    # Part 2
    # index to slice array
    slice_ind = len(stacks[source-1]) - n_moves
    stacks[dest-1].extend(stacks[source-1][slice_ind:])
    for _ in range(n_moves): stacks[source-1].pop()

# recover the message
message = ""
for s in stacks:
    message += s.pop()

print(message)