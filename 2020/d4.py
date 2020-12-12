valid_ct = 0
lines = list(map(lambda x: x.strip(), open("d4_input.txt")))

fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]) # cid can be missing
valid_ecl = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def validate_height(val):
    if val.endswith("in"):
        return 59 <= int(val[:-2]) <= 76
    elif val.endswith("cm"):
        return 150 <= int(val[:-2]) <= 193
    else:
        return False

def validate_hair(val):
    return val[0] == "#" and \
           all(map(lambda x: x.isdecimal() or x in "abcdef", val[1:]))

def validate_pid(val):
    return len(val) == 9 and \
           all(map(lambda x: x.isdecimal(), val))

i = 0
while i < len(lines):
    passport = dict()
    while i < len(lines) and lines[i] != "":
        for entry in lines[i].split(" "):
            key, val = tuple(entry.split(":"))
            passport[key] = val
        i+=1
    if set(passport.keys()).issuperset(fields) and \
       1920 <= int(passport['byr']) <= 2002 and \
       2010 <= int(passport['iyr']) <= 2020 and \
       2020 <= int(passport['eyr']) <= 2030 and \
       validate_height(passport['hgt']) and \
       validate_hair(passport['hcl']) and \
       passport['ecl'] in valid_ecl and \
       validate_pid(passport['pid']): valid_ct+=1
    i += 1

print(valid_ct)