fields = dict()
my_ticket = list()

f = open("d16_input.txt")
line = next(f)
while line != "\n":
    line = line.strip()
    key, ranges = line.split(": ")
    ranges = ranges.split(" or ")
    ranges = [list(map(int, token.split("-"))) for token in ranges]
    fields[key] = ranges
    line = next(f)
next(f) # skip the "your ticket:" label
my_ticket = list(map(int, next(f).strip().split(",")))

next(f) # skip the newline
next(f) # skip the "other tickets:" label
invalid_sum = 0
valid_tix = list()
for line in f:
    ticket_valid = True
    this_ticket = list(map(int, line.strip().split(",")))
    for value in this_ticket:
        is_valid = False
        for key in fields:
            for rang in fields[key]:
                if rang[0] <= value <= rang[1]: is_valid = True
        if not is_valid: ticket_valid = False
    if ticket_valid: valid_tix.append(this_ticket.copy())

def check_in_range(ranges, value):
    return (ranges[0][0] <= value <= ranges[0][1]) or \
           (ranges[1][0] <= value <= ranges[1][1])

possible_field_positions = {key: set() for key in fields}
for key in fields:
    for i in range(len(valid_tix[0])):
        field_matches = True
        for ticket in valid_tix:
            if not check_in_range(fields[key], ticket[i]):
                field_matches = False
                break
        if field_matches:
            possible_field_positions[key].add(i)

field_positions = dict()
while len(field_positions) < len(possible_field_positions):
    for key in possible_field_positions:
        if len(possible_field_positions[key]) == 1:
            value = possible_field_positions[key].pop()
            field_positions[key] = value
            for key2 in possible_field_positions:
                if key != key2 and value in possible_field_positions[key2]:
                    possible_field_positions[key2].remove(value)

product = 1
for key in field_positions:
    if "departure" in key:
        product *= my_ticket[field_positions[key]]
print(product)