lines = map(str.strip, open("d14_input.txt"))

racetime = 2503 # seconds
reindict = dict()
scores = dict()
for line in lines:
    tokens = line.split(" ")
    name = tokens[0]
    speed = int(tokens[3])
    runtime = int(tokens[6])
    resttime = int(tokens[-2])
    reindict[name] = (speed, runtime, resttime)
    scores[name] = 0

def get_leader(reindict, t):
    maxdist = 0
    leader = None
    for key in reindict:
        speed, runtime, resttime = reindict[key]
        cycletime = runtime + resttime
        cycledist = runtime * speed
        cycle_n = t // cycletime
        remtime = t % cycletime
        dist = cycledist * cycle_n + speed * min(runtime, remtime)
        if dist > maxdist:
            leader, maxdist = key, dist
    return leader

for i in range(1, racetime+1):
    leader = get_leader(reindict, i)
    scores[leader] += 1

print(max(scores.values()))