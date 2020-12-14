lines = map(lambda x: x.strip(), open("d5_input.txt"))

ct = 0
# part 1
'''
for line in lines:
    if any(x in line for x in ["ab", "cd", "pq", "xy"]): continue
    if sum(line.count(v) for v in "aeiou") < 3: continue
    if all(line[i] != line[i+1] for i in range(0, len(line)-1)): continue
    ct+=1
'''

# part 2
for line in lines:
    # check for at least two pairs 
    if all(line.count(line[i:i+2]) < 2 for i in range(0, len(line)-1)): continue
    if not any(line[i] == line[i+2] != line[i+1] for i in range(0, len(line)-2)): continue
    ct+=1

print(ct)