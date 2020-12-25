import json

tree = json.loads(next(open("d12_input.txt"))) # file is 1 line

def sumTree(node):
    if isinstance(node, int):
        return node
    elif isinstance(node, str):
        return 0
    elif isinstance(node, list):
        return sum(sumTree(child) for child in node)
    elif isinstance(node, dict):
        # part1: remove this if statement
        if "red" in node.keys() or "red" in node.values():
            return 0
        ret = 0
        for key in node:
            if isinstance(key, int): ret += key
            ret += sumTree(node[key])
        return ret

print(sumTree(tree))