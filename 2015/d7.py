lines = map(str.strip, open("d7_input.txt"))
max_val = 65536
wires = dict()
for line in lines:
    expr, key = line.split(" -> ")
    wires[key] = expr
# Part 2: override b with the answer to part 1
wires['b'] = 956

def isint(s):
    if s[0] == "-":
        return s[1:].isdigit()
    else:
        return s.isdigit()

def evalWire(key):
    if key.isdigit():
        # this is a constant
        return int(key)
    if not isinstance(wires[key], str):
        # this wire was already evaluated
        return wires[key]
    else:
        # this wire needs to be evaluated
        tokens = wires[key].split(" ")
        while len(tokens) < 3: tokens.insert(0, None)
        l, op, r = tuple(tokens)
        
        if op is None:
            wires[key] = evalWire(r)
            return wires[key]
        # parse the operands
        if l is not None and l.isdigit(): 
            lval = int(l)
        elif l is not None:
            lval = wires[l] if isinstance(wires[l], int) else evalWire(l)
        if r is not None and r.isdigit(): 
            rval = int(r)
        elif r is not None:
            rval = wires[r] if isinstance(wires[r], int) else evalWire(r)

        if op == "AND":
            signal = lval & rval
        elif op == "OR":
            signal = lval | rval
        elif op == "NOT":
            signal = ~rval
        elif op == "LSHIFT":
            signal = lval << rval
        elif op == "RSHIFT":
            signal = lval >> rval
        else:
            raise ValueError("Unrecognized operator: {}".format(op))
        
        signal %= max_val # prevent negatives
        wires[key] = signal
        return signal
    
print(evalWire("a"))