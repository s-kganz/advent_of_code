lines = list(map(lambda x: x.strip(), open("d6_input.txt")))

q_ct = 0
i = 0
while i < len(lines):
    answers = set(lines[i])
    while i < len(lines) and lines[i] != "":
        answers = answers.intersection(set(lines[i]))
        i+=1
    q_ct += len(answers)
    i+=1

print(q_ct)