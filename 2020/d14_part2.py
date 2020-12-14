lines = list(map(str.strip, open("d14_input.txt")))
memory = dict()

highest_bit = 35

def setBit(x, i):
    # set the ith bit to 1
    mask = 1 << i
    return x | mask

def clearBit(x, i):
    # set the ith bit to 0
    mask = ~pow(2, i)
    return x & mask

def applyFloatingBits(address, val, floatBits, i):
    if i < len(floatBits):
        # recursive case
        bit = floatBits[i]
        applyFloatingBits(setBit(address, bit), val, floatBits, i+1)
        applyFloatingBits(clearBit(address, bit), val, floatBits, i+1)
    else:
        # base case
        memory[address] = val

mask = None
floatBits = list()
for line in lines:
    command, _, op = line.split(" ")
    if command == 'mask':
        mask = op
        floatBits = [highest_bit - i for i in range(len(mask)) if mask[i] == "X"]
        maskstr = "".join("0" if char == "X" else char for char in mask)
        mask = int(maskstr, 2)
    else:
        value = int(op)
        lbracket = command.index("[")
        rbracket = command.index("]")
        address = int(command[lbracket+1:rbracket])
        address = address | mask
        applyFloatingBits(address, value, floatBits, 0)

print(sum(memory.values()))