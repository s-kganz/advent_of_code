lines = list(map(lambda x: int(x.strip()), open("d9_input.txt")))
target_number = 1309761972

i = 0
j = 1
while j < len(lines) and i != j:
    subset = lines[i:j+1]
    if sum(subset) == target_number:
        print(min(subset) + max(subset))
        break
    elif sum(subset) > target_number:
        i += 1
    else:
        j += 1