rulemap = dict()
f = open("d19_input.txt")
line = next(f)
while line != "\n":
    line = line.strip()
    colind = line.index(":")
    key = int(line[:colind])
    if line[colind+2] == '"':
        rules = eval(line[colind+2:]) # drop the quotes
    else:
        rules = line[colind+2:].split(" | ")
        rules = list(map(
            lambda x: list(map(int, x.split(" "))),
            rules
        ))
    rulemap[key] = rules
    line = next(f)
messages = list(map(str.strip, f))

# rulemap[0] = [8, 11]
# strings obeying 0 are p instances of 42 followed by m instances
# of 31, where p > m
rulemap[8]  = [[42], [42, 8]]
rulemap[11] = [[42, 31], [42, 11, 31]]

def passes_rule(root, message):
    # return the number of characters matched, -1 if no match
    ruleset = rulemap[root]
    if type(ruleset) == str:
        return 1 if message[0] == ruleset else -1
    else:
        for rulelist in ruleset:
            i = 0
            failed = False
            for rule in rulelist:
                if i >= len(message):
                    failed = True
                    break
                result = passes_rule(rule, message[i:])
                if result == -1: # next rule could not match
                    failed = True
                    break
                i += result
            if not failed:
                return i
        # no rulelists passed
        return -1

def apply_31(message, n):
    # applies rule 31 up to n times, exclusive
    # stops if a match is found or when the message does not match
    i = 0
    for _ in range(n-1):
        result = passes_rule(31, message[i:])
        if result == -1: return -1
        else: i += result
        
        if i == len(message): # match found!
            return len(message)
    return -1 # could not match with [1...n-1] instances of 31

ct_matches = 0
for message in messages:
    i = 0
    ct_42 = 0
    while i < len(message):
        result = passes_rule(42, message[i:])
        if result == -1: 
            break # failed
        else:
            i += result
            ct_42 += 1
        
        # try adding 31
        if ct_42 >= 2 and (i + apply_31(message[i:], ct_42)) == len(message):
            ct_matches += 1 # matched!
            break

print(ct_matches)