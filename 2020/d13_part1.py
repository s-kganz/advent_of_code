import math

wait, buses = tuple(map(str.strip, open("d13_input.txt")))
wait = int(wait)
buses = list(map(int, filter(lambda x: x != "x", buses.split(","))))

mindiff = math.ceil(wait / buses[0]) * buses[0] - wait
mini = 0
for i in range(len(buses)):
    diff = math.ceil(wait / buses[i]) * buses[i] - wait
    if diff < mindiff:
        mindiff = diff
        mini = i

print(mindiff * buses[mini])