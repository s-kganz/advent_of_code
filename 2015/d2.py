lines = map(lambda x: tuple(map(int, x.strip().split("x"))), open("d2_input.txt"))

'''
# Part 1: wrapping paper
tot_sqft = 0
for entry in lines:
    l, w, h = entry
    small_side = min(l * w, l * h, w * h)
    tot_sqft += (small_side + 2 * l * w + 2 * l * h + 2 * w * h)
'''

# Part 2: ribbon
tot_ft = 0
for entry in lines:
    l, w, h = entry
    bow = l * w * h
    perim = min(l+w, l+h, w+h) * 2
    tot_ft += bow + perim

print(tot_ft)