import operator
from scipy import optimize

op_dict = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

inverse_dict = {
    # l/r = side of thing you are solving for in original
    # operation.
    'l': {
        operator.add: lambda x,b: x - b,
        operator.sub: lambda x,b: x + b,
        operator.mul: lambda x,b: x / b,
        operator.truediv: lambda x,b: x * b
    },
    'r': {
        operator.add: lambda x,b: x - b,
        operator.sub: lambda x,b: b - x,
        operator.mul: lambda x,b: x / b,
        operator.truediv: lambda x,b: b / x
    }
}

def get(monkey_dict, key):
    if key not in monkey_dict:
        print("Unrecognized key: ", key)
    if not isinstance(monkey_dict[key], tuple):
        return monkey_dict[key]
    else:
        key1, op, key2 = monkey_dict[key]
        return float(op(
            get(monkey_dict, key1),
            get(monkey_dict, key2)
        ))


def depends_on(monkey_dict, parent, child):
    # Determine if the key `child` appears in the tree starting
    # at `monkey_dict[parent]`
    if not isinstance(monkey_dict[parent], tuple):
        return False
    elif child in monkey_dict[parent]:
        return True
    else:
        key1, _, key2 = monkey_dict[parent]
        return (
            depends_on(monkey_dict, key1, child) or
            depends_on(monkey_dict, key2, child)
        )

monkey_dict = dict()

# populate the dictionary
for line in open("2022/d21_input.txt").readlines():
    key, val = line.split(":")
    val_tokens = val.strip().split(" ")
    if len(val_tokens) == 1:
        monkey_dict[key] = int(val_tokens[0])
    else:
        monkey_dict[key] = (
            val_tokens[0],
            op_dict[val_tokens[1]],
            val_tokens[2]
        )

# Part 1
# print(get(monkey_dict, "root"))

# Part 2
# Solve all keys that do not depend on the `humn` key
for key in monkey_dict:
    if not depends_on(monkey_dict, key, "humn"):
        monkey_dict[key] = get(monkey_dict, key)

# verify that all non-root tuple keys are connected to at least one leaf node
for key in monkey_dict:
    if key == "root" or not isinstance(monkey_dict[key], tuple): continue
    a, _, b = monkey_dict[key]
    if isinstance(monkey_dict[a], tuple) and isinstance(monkey_dict[b], tuple):
        print("{} is not connected to a leaf node".format(key))


if isinstance(monkey_dict[monkey_dict["root"][0]], float):
    x = monkey_dict[monkey_dict["root"][0]]
    iter_key = monkey_dict["root"][2]
else:
    x = monkey_dict[monkey_dict["root"][2]]
    iter_key = monkey_dict["root"][0]

while True:
    a, forward_op, b = monkey_dict[iter_key]
    if a == "humn" or isinstance(monkey_dict[a], tuple):
        int_key, next_key = b, a
        side = "l"
    else:
        int_key, next_key = a, b
        side = "r"
    
    inverse_op = inverse_dict[side][forward_op]

    # apply the inverse operation
    x = inverse_op(x, monkey_dict[int_key])
    
    # break if we reached the `humn` key
    if a == "humn" or b == "humn":
        break

    iter_key = next_key

print("Value of humn: ", x)