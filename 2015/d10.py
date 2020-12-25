phrase = "1113222113"
for _ in range(50): #part1: 40
    new_phrase = ""
    i = 0
    run_len = 0
    current_num = phrase[i]
    while i < len(phrase):
        if phrase[i] == current_num:
            run_len += 1
        else:
            new_phrase += str(run_len) + current_num
            current_num = phrase[i]
            run_len = 1
        i += 1
    phrase = new_phrase + str(run_len) + current_num
print(len(phrase))
    