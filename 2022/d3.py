from uuid import RFC_4122


alphabet = "abcdefghijklmnopqrstuvwxyz"
priority = alphabet + alphabet.upper()

tot_priority = 0

# part 1
'''
for line in open("2022/d3_input.txt").readlines():
    line = line.strip()
    middle = len(line) // 2
    comp1 = line[:middle]
    comp2 = line[middle:]
    error_char = list(set(comp1).intersection(set(comp2)))[0]
    tot_priority += priority.index(error_char)+1
'''

# part 2
lines = [line.strip() for line in open("2022/d3_input.txt").readlines()]
i = 0
while i < len(lines):
    r1 = lines[i]
    r2 = lines[i+1]
    r3 = lines[i+2]

    badge = list(set(r1).intersection(set(r2)).intersection(set(r3)))[0]
    tot_priority += priority.index(badge)+1

    i += 3

print(tot_priority)
