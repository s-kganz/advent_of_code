lines = list(map(lambda x: x.strip(), open("d7_input.txt")))
rules = dict() # key bags are contained by value bags

# populate the rules
for line in lines:
    key, values = line.split(" bags contain ")
    values = list(map(lambda x: " ".join(x.split(" ")[1:3]), values.split(", ")))
    for val in values:
        if val in rules:
            rules[val].append(key)
        else:
            rules[val] = [key]
rules["other bags."] = list()

this_layer = rules["shiny gold"]
seen_bags = set(this_layer) # bags that can eventually contain a shiny gold
next_layer = set()
color_ct = 0

while len(this_layer) != 0:
    color_ct += len(this_layer)
    for parent in this_layer:
        if parent not in rules: continue
        for child in rules[parent]:
            if child not in seen_bags:
                next_layer.add(child)
            seen_bags.add(child)
    this_layer = list(next_layer)
    next_layer.clear()

print(color_ct)