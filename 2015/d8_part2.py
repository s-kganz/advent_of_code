import re
lines = map(str.strip, open("d8_input.txt"))

orig_total = 0
new_total = 0
for line in lines:
    L =  len(line)
    new_line = L + 2 + line.count("\\") + line.count('"')

    new_total += new_line
    orig_total += L

print(new_total - orig_total)