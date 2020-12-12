jolts = list(map(lambda x: int(x.strip()), open("d10_input.txt")))
jolts.append(max(jolts)+3)
jolts.insert(0, 0)
jolts.sort()

lookup = {0: 1}

def countPathways(node):
    connections = list(filter(lambda x: x < node and x >= node-3, jolts))
    paths = 0
    for conn in connections:
        if conn in lookup:
            paths += lookup[conn]
        else:
            paths += countPathways(conn)
    lookup[node] = paths
    return paths

print(countPathways(max(jolts)))