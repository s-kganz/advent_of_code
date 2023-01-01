# Following along with a solution by /u/Derailed_Dash
from itertools import cycle

def mix(data, n=1):
    # Copy the input array to maintain the mixing order when mixing
    # multiple times.
    mixed = [a for a in enumerate(data)]
    cyc = cycle(mixed.copy())
    # Subtract 1 since we will remove a tuple during the mix process.
    len_mixed = len(mixed)-1
    for _  in range(len(mixed) * n):
        to_mix = next(cyc)
        old_idx = mixed.index(to_mix)
        mixed.remove(to_mix)
        new_idx = (old_idx + to_mix[1] + len_mixed) % len_mixed
        mixed.insert(new_idx, to_mix)
    
    return mixed


with open("2022/d20_input.txt") as f:
    data = list(map(lambda x: int(x.strip()), f.readlines()))

mixed = mix(data)
zero_index = [m[1] for m in mixed].index(0)
part1_out = sum(mixed[(zero_index + i) % len(mixed)][1] for i in (1000, 2000, 3000))
print("Part 1:", part1_out)

dec_key = 811589153
n_mixes = 10
new_data = [d * dec_key for d in data]
new_mixed = mix(new_data, n=n_mixes)
zero_index = [m[1] for m in new_mixed].index(0)
part2_out = sum(new_mixed[(zero_index + i) % len(new_mixed)][1] for i in (1000, 2000, 3000))
print("Part 2:", part2_out)
