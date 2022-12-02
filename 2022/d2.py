opp_moves = "ABC"
my_moves  = "XYZ"

def play_round(line):
    line = line.strip()
    opp_move = opp_moves.index(line[0])
    my_move  = my_moves.index(line[2])

    if my_move == (opp_move + 1) % 3:
        # I win
        return (opp_move+1, my_move+1+6)
    elif my_move == opp_move:
        # draw
        return (opp_move+1+3, my_move+1+3)
    else:
        # I lose
        return (opp_move+1+6, my_move+1)

# Part 2
def pick_move(line):
    shift = my_moves.index(line[2])-1
    opp_move = opp_moves.index(line[0])

    return my_moves[(opp_move + shift)%3]

my_score = 0
with open("2022/d2_input.txt") as f: 
    for line in f.readlines():
        # Part 1
        # my_score += play_round(line)[1]
        # Part 2
        my_score += play_round(line[0] + " " + pick_move(line))[1]
print(my_score)
