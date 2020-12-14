routes = dict()
for line in map(str.strip, open("d9_input.txt")):
    tokens = line.split(" ")
    orig, dest, dist = tokens[0], tokens[2], int(tokens[4])
    if orig in routes:
        routes[orig].append((dest, dist))
    else:
        routes[orig] = [(dest, dist)]
    if dest in routes:
        routes[dest].append((orig, dist))
    else:
        routes[dest] = [(orig, dist)]

routes["root"] = [(key, 0) for key in routes.keys()]

def get_min_path(node, seen):
    '''
    node: current location
    cumdist: distance traveled to this point
    seen: list of nodes visited
    '''
    mindist = None
    seen.append(node)
    if len(seen) == len(routes.keys()):
        return 0 # trip is done
    
    for tup in routes[node]:
        key, dist = tup
        if key != node and key not in seen:
            # can travel down this path
            newdist = get_min_path(key, seen) + dist
            if mindist is None: mindist = newdist
            else: mindist = min(mindist, newdist)
    seen.pop()
    return mindist

print(get_min_path("root", []))