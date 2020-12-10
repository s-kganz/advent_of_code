jolts = list(map(lambda x: int(x.strip()), open("d10_input.txt")))
jolts.append(max(jolts)+3)
jolts.insert(0, 0)
jolts.sort()

d3_ct = 0
d1_ct = 0
diffs = (jolts[i+1] - jolts[i] for i in range(0, len(jolts)-1))
for diff in diffs:
    if diff == 1: d1_ct+=1
    elif diff == 3: d3_ct+=1

print(d1_ct * d3_ct)