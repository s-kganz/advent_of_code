possible_allergens = dict()
ingredient_counts = dict()
all_ingredients = set()

this_ingredients = set()
this_allergens = list()
is_ingredient = True
for line in open("d21_input.txt"):
    tokens = line.strip().split(" ")
    for token in tokens:
        if token[0] == "(":
            is_ingredient = False
            continue
        if is_ingredient:
            if token in ingredient_counts:
                ingredient_counts[token] += 1
            else:
                ingredient_counts[token] = 1
            this_ingredients.add(token)
        else:
            this_allergens.append(token[:-1])
            if token[-1] == ")": 
                is_ingredient = True
                for allergen in this_allergens:
                    if allergen in possible_allergens:
                        possible_allergens[allergen] = \
                            possible_allergens[allergen].intersection(this_ingredients)
                    else:
                        possible_allergens[allergen] = this_ingredients.copy()
                all_ingredients = all_ingredients.union(this_ingredients)
                this_ingredients.clear()
                this_allergens.clear()

maybe_allergens = set()
for s in possible_allergens.values():
    maybe_allergens = maybe_allergens.union(s)

# part 1 answer
'''
not_allergens = all_ingredients - maybe_allergens
print(sum(ingredient_counts[ing] for ing in not_allergens))
'''
while any(len(val) > 1 for val in possible_allergens.values()):
    for key in possible_allergens:
        if len(possible_allergens[key]) == 1:
            for key2 in possible_allergens:
                if key != key2:
                    possible_allergens[key2] -= possible_allergens[key]

print(",".join(list(possible_allergens[key])[0] for key in sorted(list(possible_allergens.keys()))))

