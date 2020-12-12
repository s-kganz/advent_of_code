lines = list(map(lambda x: x.strip(), open("d7_input.txt")))
rules = dict() # key bags contain value bags

def parseNumColor(string):
    tokens = string.split(" ")
    return [int(tokens[0]), " ".join(tokens[1:3])]

def countTotalBags(key):
    ct = 0
    for child in rules[key]:
        ct += child[0] * (1+ countTotalBags(child[1]))
    return ct

for line in lines:
    key, values = line.split(" bags contain ")
    if values == "no other bags.": 
        rules[key] = list()
        continue

    values = list(map(parseNumColor, values.split(", ")))
    rules[key] = values

print(countTotalBags("shiny gold"))