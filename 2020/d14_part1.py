lines = list(map(str.strip, open("d14_input.txt")))
memory = dict()

def applyMask(mask, op):
    # convert op to binary representation
    opbin = []
    for i in range(35, -1, -1):
        if op >= pow(2, i):
            opbin.append(1)
            op -= pow(2, i)
        else:
            opbin.append(0)
    for i in range(len(mask)):
        if mask[i] not in "10": continue
        else: opbin[i] = int(mask[i])
    # convert back to decimal
    dec = sum(pow(2, 35-i) if opbin[i] else 0 for i in range(len(opbin)))
    return dec      

mask = None
for line in lines:
    command, _, op = line.split(" ")
    if command == 'mask':
        mask = op
    else:
        lbracket = command.index("[")
        rbracket = command.index("]")
        address = int(command[lbracket+1:rbracket])
        value = applyMask(mask, int(op))
        memory[address] = value

print(sum(memory.values()))