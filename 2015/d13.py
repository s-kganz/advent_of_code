hapmap = dict()
for line in map(str.strip, open("d13_input.txt")):
    tokens = line.split(" ")
    sign = 1 if tokens[2] == "gain" else -1
    a = tokens[0]
    b = tokens[-1][:-1] # drop the period
    if a not in hapmap:
        hapmap[a] = dict()
    hapmap[a][b] = int(tokens[3]) * sign
# Remove "me" from dict for part 1
hapmap["Me"] = {person: 0 for person in hapmap.keys()}
for key in hapmap:
    hapmap[key]["Me"] = 0

arrs = 0
people = list(hapmap.keys())
def testArrangement(arr):
    if len(arr) == len(people):
        hap = 0
        for i in range(len(arr)):
            hap += hapmap[arr[i]][arr[(i+1) % len(arr)]]
            hap += hapmap[arr[i]][arr[(i-1) % len(arr)]]
        return hap
    else:
        maxhap = -9999
        for person in people:
            if person not in arr:
                arr.append(person)
                maxhap = max(maxhap, testArrangement(arr))
                arr.pop()
        return maxhap

print(testArrangement([]))