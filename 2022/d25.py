from math import log, ceil

VALUE_LOOKUP = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    "=": -2
}

# Inverse of the above dict
CHAR_LOOKUP = {
    VALUE_LOOKUP[key]:key for key in VALUE_LOOKUP
}

def snafu_to_decimal(snafu):
    out = 0
    for i in range(len(snafu)):
        power = len(snafu) - i - 1
        out += VALUE_LOOKUP[snafu[i]] * (5 ** power)
    return out

def decimal_to_snafu(snafu, decimal, power):
    if decimal == 0: 
        # This is a valid representation
        return True
     
    if power < 0:
        # Representation must be correct
        return decimal == 0

    for next_digit in [-2, -1, 0, 1, 2]:
        next_sub = (5 ** power) * next_digit
        next_decimal = decimal - next_sub
        if abs(next_decimal) > abs(3 * (5 ** (power-1)) - 1):
            # Current character should not be accepted.
            continue
        else:
            # Next state is possibly valid, write it and recurse
            index = len(snafu) - power - 1
            snafu[index] = CHAR_LOOKUP[next_digit]
            if decimal_to_snafu(snafu, next_decimal, power-1):
                return True
            else:
                # Reset state, try next digit
                snafu[index] = '0'

    
    # No valid state was found
    return False

def decimal_to_snafu_driver(decimal):
    # 0 is an edge case because log fails
    if decimal == 0:
        return '0'

    init_snafu = ['0'] * (ceil(log(decimal, 5))+1)
    decimal_to_snafu(init_snafu, decimal, len(init_snafu)-1)
    return "".join(init_snafu).lstrip('0')

def read_puzzle(fname):
    with open(fname) as f:
        nums = list(map(str.strip, f.readlines()))
    return nums

nums_snafu = read_puzzle("2022/d25_input.txt")
input_decimal = sum(map(snafu_to_decimal, nums_snafu))
input_snafu = decimal_to_snafu_driver(input_decimal)

print("Part 1:", input_snafu)