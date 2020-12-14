import re
lines = map(str.strip, open("d8_input.txt"))

match_hex = re.compile("[^\\\\]\\\\x[a-f0-9]{2}")
match_slash = re.compile("\\\\\\\\")
match_quote = re.compile("\\\\\"")

tot_chars = 0
in_mem = 0
for line in lines:
    L = len(line)
    tot_chars += L
    slash_matches = len(re.findall(match_slash, line))
    line = line.replace("\\\\", "\\")
    hex_matches = len(re.findall(match_hex, line))
    quote_matches = len(re.findall(match_quote, line))
    line_in_mem = (L - 2 - (hex_matches*3) - slash_matches - quote_matches)
    in_mem += line_in_mem
    print(L, line_in_mem)

print(tot_chars - in_mem)



