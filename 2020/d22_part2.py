def get_score(hand):
    score = 0
    for i in range(len(hand)):
        score += hand[i] * (len(hand)-i)
    return score

def hash_hands(p1, p2):
    return hash("".join(map(str, p1+[1]+p2)))

def do_combat(p1, p2):  
    game_hashes = set()
    while len(p1) > 0 and len(p2) > 0:
        h = hash_hands(p1, p2)
        c1, c2 = p1.pop(0), p2.pop(0)
        if h in game_hashes:
            # this state was seen before
            return True
        elif c1 <= len(p1) and c2 <= len(p2):
            new_p1 = p1[0:c1].copy()
            new_p2 = p2[0:c2].copy()
            round_won = do_combat(new_p1, new_p2)
        else:
            round_won = c1 > c2
        
        if round_won:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
        
        # update the set of states
        game_hashes.add(h)
    return len(p1) > 0
    
f = open("d22_input.txt")
next(f) # skip the player label
p1 = []
line = next(f)
while line != "\n":
    p1.append(int(line.strip()))
    line = next(f)
next(f) # skip the blank
p2 = []
line = next(f)
while line.strip().isdigit():
    p2.append(int(line.strip()))
    try:
        line = next(f)
    except StopIteration:
        break

print(p1)
print(p2)

if do_combat(p1, p2):
    print(get_score(p1))
else:
    print(get_score(p2))