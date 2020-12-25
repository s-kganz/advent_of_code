from collections import deque

f = open("d22_input.txt")
next(f) # skip the player label
p1 = []
line = next(f)
while line != "\n":
    p1.append(int(line.strip()))
    line = next(f)
next(f) # skip the blank
p2 = []
line = next(f)
while line.strip().isdigit():
    p2.append(int(line.strip()))
    try:
        line = next(f)
    except StopIteration:
        break

p1 = deque(p1)
p2 = deque(p2)

while len(p1) > 0 and len(p2) > 0:
    c1, c2 = p1.popleft(), p2.popleft()
    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)

windeck = list(p2) if len(p2) > 0 else list(p1)
score = 0
for i in range(len(windeck)):
    score += windeck[i] * (len(windeck) - i)
print(score)