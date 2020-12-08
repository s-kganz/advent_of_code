lines = list(map(lambda x: x.strip(), open("d8_input.txt")))

def run_instructions(instructions):
    seen_lines = set()
    i = 0
    acc = 0
    while i < len(instructions):
        if i in seen_lines: return None
        op, val = instructions[i].split(" ")
        val = int(val)
        seen_lines.add(i)
        if op == "acc":
            acc += val
            i += 1
        elif op == "jmp":
            i += val
        else:
            i += 1
    return acc

i = 0
while i < len(lines):
    if not lines[i].startswith("acc"):
        old_inst = lines[i]
        if lines[i].startswith("nop"):
            lines[i] = lines[i].replace("nop", "jmp")
        else:
            lines[i] = lines[i].replace("jmp", "nop")
        result = run_instructions(lines)
        if result is not None: 
            print(result)
        else:
            lines[i] = old_inst
    i += 1
