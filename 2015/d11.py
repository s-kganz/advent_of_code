import re

pattern_pair = re.compile("([a-z])\\1")
alphabet = "abcdefghijklmnopqrstuvwxyz"

def validate_pass(s):
    as_num = list(map(lambda c: alphabet.index(c), s))
    if not any(as_num[i] == as_num[i+1]-1 == as_num[i+2]-2 for i in range(0, len(as_num)-2)):
        return False
    if len(set(re.findall(pattern_pair, s))) < 2:
        return False
    return True

def increment_pass(s, i):
    new_ind = alphabet.index(s[i])+1
    s[i] = alphabet[new_ind % len(alphabet)]
    if new_ind == 26:
        return "".join(increment_pass(s, i-1))
    return "".join(s)

    
start = increment_pass(list("cqjxxyzz"), 7) # part 1; "cqjxjnds"
while not validate_pass(start):
    start = increment_pass(list(start), len(start)-1)
    start = start.replace("i", "j").replace("o", "p").replace("l", "m")

print(start)