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
            
print(sum(passes_rule(0, message) == len(message) for message in messages))