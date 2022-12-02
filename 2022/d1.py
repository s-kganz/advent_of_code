with open("2022/d1/d1_input.txt") as f:
    inp = f.read().strip()

cals = [
    sum(map(lambda x: int(x.strip()), item.split("\n"))) 
    for item in inp.split("\n\n")
]
cals.sort()
print(sum(cals[-3:]))