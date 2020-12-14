import hashlib

key = "bgvyzdsv"

i = 1
while True:
    inp = key + str(i)
    result = hashlib.md5(inp.encode("utf-8")).hexdigest()
    if result[:6] == "000000":
        break
    i += 1

print(i)