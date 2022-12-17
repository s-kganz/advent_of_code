def compare_inputs(l, r):
    if type(l) == int and type(r) == int:
        if l == r:
            return 0
        else:
            return 1 if l < r else -1
    elif type(l) == int and type(r) == list:
        return compare_inputs([l], r)
    elif type(l) == list and type(r) == int:
        return compare_inputs(l, [r])
    else:
        for i in range(min(len(r), len(l))):
            # Compare each element
            result = compare_inputs(l[i], r[i])
            if result != 0: return result
        # No decision made
        if len(l) == len(r):
            return 0
        else:
            return 1 if len(l) < len(r) else -1

idx = 1
total = 0
# Initialize the list of packets for the second part
packets = list()
for pair in open("2022/d13_input.txt").read().split("\n\n"):
    print(idx, end=" ")
    l1, l2 = tuple(map(lambda x: eval(x.strip()), pair.split("\n")))
    result = compare_inputs(l1, l2)
    if result == 1:
        print("In order")
        total += idx
    elif result == -1:
        print("Out of order")
    else:
        print("/shrug")
    idx += 1
    packets.append(l1)
    packets.append(l2)

# Part 1
print("Part 1 answer:\t", total)

# Part 2
# Sum the number of packets less than the dividers
dividers = [
    [[2]], [[6]]
]
prod = 1
for i in range(len(dividers)):
    prod *= (sum(compare_inputs(p, dividers[i]) == 1 for p in packets)+1+i)

print("Part 2 answer:\t", prod)
