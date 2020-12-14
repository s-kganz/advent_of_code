from functools import reduce

_, buses = tuple(map(str.strip, open("d13_input.txt")))
buses = buses.split(",")
indexes = [i for i in range(len(buses)) if buses[i].isdigit()]
n = list(map(int, filter(lambda x: x != 'x', buses)))
a = [(ni - ii)%ni for ni, ii in zip(n, indexes)]
print(n, a)

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for ni, ai in zip(n, a):
        p = prod // ni
        sum += ai * mul_inv(p, ni) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q*x0, x0
    if x1 < 0: x1 += b0
    return x1

print(chinese_remainder(n, a))

