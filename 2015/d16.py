target_sue = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}
i = 1
for line in map(str.strip, open("d16_input.txt")):
    this_sue = dict()
    for datapair in line[line.index(":")+2:].split(", "):
        key, val = datapair.split(": ")
        val = int(val)
        if val == 0: continue # don't know the true value
        this_sue[key] = val
    # check if a key fails
    matched = True
    for key in this_sue:
        if key in ["cats", "trees"] and target_sue[key] <= this_sue[key]:
            matched = False
        elif key in ["pomeranians", "goldfish"] and target_sue[key] >= this_sue[key]:
            matched = False
        elif this_sue[key] != target_sue[key]:
            matched = False
        
    if matched: print(i)
    i += 1