lines = list(map(lambda x: int(x.strip()), open("d9_input.txt")))
for i in range(25, len(lines)):
    prev_25 = lines[i-25:i]
    found = False
    for j in range(25):
        if found: break
        for k in range(j, 25):
            if prev_25[j] + prev_25[k] == lines[i]:
                found = True
                break
    if not found: print(lines[i])   