pwds = map(lambda x: x.strip(), list(open("d2_input.txt")))

valid_ct = 0

for line in pwds:
    policy, letter, pwd = tuple(line.split(" "))
    low, high = tuple(map(int, policy.split("-")))
    letter = letter[0] # drop colon
    # Part 1
    if low <= pwd.count(letter) <= high: valid_ct += 1
    # Part 2
    # if (pwd[low-1] == letter) != (pwd[high-1] == letter): valid_ct+=1

print(valid_ct)